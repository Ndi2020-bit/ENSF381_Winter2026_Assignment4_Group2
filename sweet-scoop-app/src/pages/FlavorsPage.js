// src/pages/FlavorsPage.js
import React, { useState } from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import FlavorCatalog from "../components/FlavorCatalog";
import OrderList from "../components/OrderList";

function FlavorsPage() {
  const [order, setOrder] = useState([]);

  const addToOrder = (flavor) => {
    setOrder((prev) => {
      const exist = prev.find((item) => item.id === flavor.id);
      if (exist) {
        return prev.map((item) =>
          item.id === flavor.id ? { ...item, quantity: item.quantity + 1 } : item
        );
      } else {
        return [...prev, { ...flavor, quantity: 1 }];
      }
    });
  };

  return (
    <div className="flavors-page">
      <Header />
      <div className="content">
        <FlavorCatalog addToOrder={addToOrder} />
        <OrderList order={order} setOrder={setOrder} />
      </div>
      <Footer />
    </div>
  );
}

export default FlavorsPage;