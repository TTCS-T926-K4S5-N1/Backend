package com.crm.controller.products;

import com.crm.service.products.ProductService;
import java.io.IOException;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;

@WebServlet("/products")
public class ProductServlet extends HttpServlet {
    private ProductService productService = new ProductService();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        HttpSession session = request.getSession();
        String role = (String) session.getAttribute("role"); 
        boolean isSalesDirector = "SalesDirector".equals(role);
        
        request.setAttribute("isSalesDirector", isSalesDirector);
        request.getRequestDispatcher("/jsp/products/product-list.jsp").forward(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        String action = request.getParameter("action");
        if ("delete".equals(action)) {
            int productId = Integer.parseInt(request.getParameter("id"));
            String message = productService.deleteProductLogic(productId);
            request.getSession().setAttribute("alertMessage", message);
            response.sendRedirect(request.getContextPath() + "/products");
        }
    }
}