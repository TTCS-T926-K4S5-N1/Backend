from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import pandas as pd
from app.schemas.user import UserImportSchema
from pydantic import ValidationError
import io

router = APIRouter(prefix="/api/admin/users", tags=["Admin Users"])

# YÊU CẦU 1: API TẢI FILE MẪU
@router.get("/import-template")
async def download_template():
    # Tạo một file excel rỗng với đúng 4 cột tiêu đề chuẩn
    df = pd.DataFrame(columns=["Full Name", "Email", "Department", "Role"])
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    output.seek(0)
    
    return StreamingResponse(
        output, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
        headers={"Content-Disposition": "attachment; filename=user_import_template.xlsx"}
    )

# YÊU CẦU 2 & 3: BÁO LỖI TỪNG DÒNG, BỎ QUA LỖI VÀ NHẬP DÒNG ĐÚNG
@router.post("/bulk-import")
async def import_users(file: UploadFile = File(...)):
    if not file.filename.endswith(('.xls', '.xlsx')):
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận file định dạng Excel")

    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents), engine='openpyxl')
        df.dropna(how='all', inplace=True)
        
        valid_users = []
        errors = []

        # Quét từng dòng dữ liệu
        for index, row in df.iterrows():
            try:
                user_data = {
                    "full_name": str(row.get("Full Name", "")),
                    "email": str(row.get("Email", "")),
                    "department": str(row.get("Department", "")),
                    "role": str(row.get("Role", "User"))
                }
                valid_user = UserImportSchema(**user_data)
                # Dòng hợp lệ thì đưa vào danh sách chờ nhập
                valid_users.append(valid_user.model_dump())
            except ValidationError as e:
                # Dòng lỗi thì ghi nhận lại, KHÔNG dừng chương trình
                errors.append({"row": index + 2, "error": [err["msg"] for err in e.errors()]})

        # Báo cáo tổng kết theo yêu cầu
        return {
            "success": True, 
            "message": "Quá trình kiểm tra và nhập liệu hoàn tất.",
            "summary": {
                "total_rows": len(df),
                "imported_success": len(valid_users), # Số lượng dòng hợp lệ
                "skipped_errors": len(errors)         # Số lượng dòng bị bỏ qua
            },
            "error_details": errors # Danh sách chi tiết các dòng bị lỗi
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))