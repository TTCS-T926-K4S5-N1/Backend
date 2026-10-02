package com.crm.model;

public class Product {
    private int id;
    private String code;
    private String name;
    private String type; // OneTime hoặc Subscription
    private String unit;
    private double listedPrice;
    private double floorPrice;
    private double costPrice;
    private boolean isActive;

    public Product() {}

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getCode() { return code; }
    public void setCode(String code) { this.code = code; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
    public String getUnit() { return unit; }
    public void setUnit(String unit) { this.unit = unit; }
    public double getListedPrice() { return listedPrice; }
    public void setListedPrice(double listedPrice) { this.listedPrice = listedPrice; }
    public double getFloorPrice() { return floorPrice; }
    public void setFloorPrice(double floorPrice) { this.floorPrice = floorPrice; }
    public double getCostPrice() { return costPrice; }
    public void setCostPrice(double costPrice) { this.costPrice = costPrice; }
    public boolean isActive() { return isActive; }
    public void setActive(boolean isActive) { this.isActive = isActive; }
}