from __future__ import annotations


def vip_discount_template(name: str, discount: int = 20) -> tuple[str, str]:
    subject = f"Exclusive offer just for you, {name}"
    html = f"""
    <html><body style='font-family: Arial, sans-serif;'>
      <h2>Thank you for being a top customer, {name}!</h2>
      <p>As one of our most valued shoppers, enjoy <strong>{discount}% OFF</strong> your next order.</p>
      <a href='#' style='background:#111;color:#fff;padding:10px 16px;text-decoration:none;border-radius:6px;'>Shop Now with VIP Discount</a>
    </body></html>
    """
    return subject, html


def winback_template(name: str, days: int) -> tuple[str, str]:
    subject = f"We miss you, {name} - here's something special"
    html = f"""
    <html><body style='font-family: Arial, sans-serif;'>
      <h2>Hi {name}, we miss you.</h2>
      <p>It's been {days} days since your last order. We added new products you'll love.</p>
      <a href='#' style='background:#0d9488;color:#fff;padding:10px 16px;text-decoration:none;border-radius:6px;'>Come Back & Save 20%</a>
    </body></html>
    """
    return subject, html


def upsell_template(name: str) -> tuple[str, str]:
    subject = "Based on your purchases, you'll love these"
    html = f"""
    <html><body style='font-family: Arial, sans-serif;'>
      <h2>{name}, your premium picks are ready.</h2>
      <p>You're a frequent shopper. Upgrade to our premium collection today.</p>
      <a href='#' style='background:#1d4ed8;color:#fff;padding:10px 16px;text-decoration:none;border-radius:6px;'>Explore Premium Products</a>
    </body></html>
    """
    return subject, html


def rfm_personalized_template(name: str, segment: str) -> tuple[str, str]:
    subject = f"{name}, offers curated for your {segment} journey"
    cta = {
        "New": "Discover Bestsellers",
        "At-Risk": "Return and Save",
        "Potential": "Unlock Member Benefits",
    }.get(segment, "Shop Recommendations")

    html = f"""
    <html><body style='font-family: Arial, sans-serif;'>
      <h2>Hi {name}, personalized for {segment} segment</h2>
      <p>We prepared recommendations based on your shopping pattern.</p>
      <a href='#' style='background:#7c3aed;color:#fff;padding:10px 16px;text-decoration:none;border-radius:6px;'>{cta}</a>
    </body></html>
    """
    return subject, html
