#!/usr/bin/env python3
"""
PowerCast Stripe Integration
Creates Stripe products and payment links for:
1. Weekly ERCOT Forecast ($99/month recurring)
2. ERCOT Dataset ($39 one-time)
3. PowerCast Bundle ($69 one-time)
"""

import os
import stripe
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

def create_powercast_products():
    """Create Stripe products and payment links for PowerCast"""

    print("Creating PowerCast products on Stripe...\n")

    # Product 1: Weekly Forecast (Recurring)
    print("1. Creating Weekly ERCOT Forecast (Subscription)...")
    product1 = stripe.Product.create(
        name="PowerCast Weekly ERCOT Forecast",
        description="AI-powered 7-day electricity price forecasts for ERCOT. Updated weekly. 8.2% MAPE accuracy.",
    )

    price1 = stripe.Price.create(
        product=product1.id,
        unit_amount=9900,  # $99.00
        currency="usd",
        recurring={"interval": "month"},
    )

    payment_link1 = stripe.PaymentLink.create(
        line_items=[{"price": price1.id, "quantity": 1}],
        after_completion={
            "type": "hosted_confirmation",
            "hosted_confirmation": {
                "custom_message": "Thank you for subscribing to PowerCast! You'll receive your first weekly forecast within 24 hours via email."
            }
        }
    )

    print(f"   Product ID: {product1.id}")
    print(f"   Price ID: {price1.id}")
    print(f"   Payment Link: {payment_link1.url}")
    print()

    # Product 2: Dataset (One-time)
    print("2. Creating ERCOT Dataset (One-time purchase)...")
    product2 = stripe.Product.create(
        name="ERCOT Electricity Price Dataset (2024-2026)",
        description="Clean, analysis-ready ERCOT LMP data with weather features. 17.5K records. Perfect for ML research.",
    )

    price2 = stripe.Price.create(
        product=product2.id,
        unit_amount=3900,  # $39.00
        currency="usd",
    )

    payment_link2 = stripe.PaymentLink.create(
        line_items=[{"price": price2.id, "quantity": 1}],
        after_completion={
            "type": "hosted_confirmation",
            "hosted_confirmation": {
                "custom_message": "Thank you for purchasing the ERCOT Dataset! Download link has been sent to your email."
            }
        }
    )

    print(f"   Product ID: {product2.id}")
    print(f"   Price ID: {price2.id}")
    print(f"   Payment Link: {payment_link2.url}")
    print()

    # Product 3: Bundle (One-time)
    print("3. Creating PowerCast Bundle (One-time purchase)...")
    product3 = stripe.Product.create(
        name="PowerCast Bundle — Dataset + Forecasts",
        description="ERCOT dataset + 1 month of weekly forecasts. Best value for traders and researchers.",
    )

    price3 = stripe.Price.create(
        product=product3.id,
        unit_amount=6900,  # $69.00
        currency="usd",
    )

    payment_link3 = stripe.PaymentLink.create(
        line_items=[{"price": price3.id, "quantity": 1}],
        after_completion={
            "type": "hosted_confirmation",
            "hosted_confirmation": {
                "custom_message": "Thank you for purchasing the PowerCast Bundle! You'll receive the dataset download link and your first forecast within 24 hours."
            }
        }
    )

    print(f"   Product ID: {product3.id}")
    print(f"   Price ID: {price3.id}")
    print(f"   Payment Link: {payment_link3.url}")
    print()

    # Summary
    print("=" * 60)
    print("STRIPE PAYMENT LINKS (copy these into dashboard/index.html):")
    print("=" * 60)
    print(f"\nWeekly Forecast: {payment_link1.url}")
    print(f"Dataset: {payment_link2.url}")
    print(f"Bundle: {payment_link3.url}")
    print()

    # Save to file for reference
    with open('stripe_payment_links.txt', 'w') as f:
        f.write("PowerCast Stripe Payment Links\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Weekly Forecast ($99/month):\n{payment_link1.url}\n\n")
        f.write(f"Dataset ($39 one-time):\n{payment_link2.url}\n\n")
        f.write(f"Bundle ($69 one-time):\n{payment_link3.url}\n\n")
        f.write("\nProduct IDs:\n")
        f.write(f"- Weekly: {product1.id}\n")
        f.write(f"- Dataset: {product2.id}\n")
        f.write(f"- Bundle: {product3.id}\n")

    print("Links saved to: stripe_payment_links.txt")

    return {
        'weekly': payment_link1.url,
        'dataset': payment_link2.url,
        'bundle': payment_link3.url,
    }

if __name__ == '__main__':
    try:
        links = create_powercast_products()
        print("\n✅ PowerCast products created successfully!")
        print("Next step: Update dashboard/index.html with these payment links")
    except stripe.error.StripeError as e:
        print(f"\n❌ Stripe API error: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
