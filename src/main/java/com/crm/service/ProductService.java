package com.crm.service.products;

import com.crm.dao.products.ProductDAO;
import java.sql.SQLException;

public class ProductService {
    private ProductDAO productDAO = new ProductDAO();

    public String deleteProductLogic(int productId) {
        try {
            if (productDAO.hasQuoteItems(productId)) {
                productDAO.deactivateProduct(productId);
                return "Sản phẩm đã xuất hiện trong báo giá. Hệ thống đã chuyển trạng thái ngừng kinh doanh.";
            }
            productDAO.deleteProduct(productId);
            return "Xoá sản phẩm thành công.";
        } catch (SQLException e) {
            e.printStackTrace();
            return "Lỗi hệ thống khi xử lý.";
        }
    }
}