from typing import List
from fastapi import APIRouter, Depends
from app.schemas.customer import CustomerResponse, CustomerCreate
from app.schemas.response import SuccessResponse
from app.dependencies.auth import get_current_user
from app.database.mock_db import get_all_customers, get_customer_by_id, MOCK_CUSTOMERS
from app.core.exceptions import NotFoundException

router = APIRouter(prefix="/crm", tags=["CRM Customers"])

@router.get("/customers", response_model=SuccessResponse[List[CustomerResponse]], summary="Lấy danh sách khách hàng")
def list_customers(current_user: dict = Depends(get_current_user)):
    """
    Lấy danh sách khách hàng trong hệ thống CRM.
    Yêu cầu đã đăng nhập (bất kỳ role nào).
    """
    customers_data = get_all_customers()
    customers = [CustomerResponse(**c) for c in customers_data]
    return SuccessResponse[List[CustomerResponse]](
        message="Lấy danh sách khách hàng thành công",
        data=customers
    )

@router.get("/customers/{customer_id}", response_model=SuccessResponse[CustomerResponse], summary="Xem chi tiết khách hàng")
def get_customer_detail(customer_id: str, current_user: dict = Depends(get_current_user)):
    """
    Xem chi tiết thông tin khách hàng theo ID.
    Nếu khách hàng không tồn tại -> ném NotFoundException (HTTP 404) kèm action: GO_BACK.
    """
    customer_data = get_customer_by_id(customer_id)
    if not customer_data:
        raise NotFoundException(
            message=f"Không tìm thấy khách hàng với mã '{customer_id}'.",
            action="GO_BACK"
        )
    
    return SuccessResponse[CustomerResponse](
        message="Lấy thông tin khách hàng thành công",
        data=CustomerResponse(**customer_data)
    )

@router.post("/customers", response_model=SuccessResponse[CustomerResponse], summary="Thêm mới khách hàng")
def create_customer(payload: CustomerCreate, current_user: dict = Depends(get_current_user)):
    """Thêm mới một khách hàng vào hệ thống CRM"""
    new_id = f"CUST{len(MOCK_CUSTOMERS) + 1:03d}"
    new_cust = {
        "id": new_id,
        "name": payload.name,
        "tax_code": payload.tax_code,
        "phone": payload.phone,
        "email": payload.email,
        "address": payload.address,
        "owner_id": current_user["username"],
        "status": "ACTIVE"
    }
    MOCK_CUSTOMERS[new_id] = new_cust
    return SuccessResponse[CustomerResponse](
        message="Tạo mới khách hàng thành công",
        data=CustomerResponse(**new_cust)
    )
