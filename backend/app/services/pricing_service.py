"""
Pricing Service.
Implements the Fair Price Engine formula.
"""

from app.schemas.pricing import FairPriceCalculateRequest, FairPriceResponse


class PricingService:
    @staticmethod
    def calculate_fair_price(req: FairPriceCalculateRequest) -> FairPriceResponse:
        """
        Calculates the fair price floor based on material, labor, and logistics.
        
        Formula:
        fair_price = material + labor_cost + dye + transport + wastage + profit
        """
        labor_cost_total = req.labor_hours * req.regional_wage_per_hour
        
        base_cost = (
            req.material_cost +
            labor_cost_total +
            req.dye_cost +
            req.transport_cost +
            req.wastage_cost
        )
        
        fair_price_floor = base_cost + req.profit_margin
        
        # Recommendations
        recommended_price = fair_price_floor * 1.15
        premium_price = fair_price_floor * 1.35
        
        breakdown = {
            "material_cost": req.material_cost,
            "labor_cost": labor_cost_total,
            "dye_cost": req.dye_cost,
            "transport_cost": req.transport_cost,
            "wastage_cost": req.wastage_cost,
            "profit_margin": req.profit_margin,
            "base_cost": base_cost
        }
        
        return FairPriceResponse(
            labor_cost_total=labor_cost_total,
            fair_price_floor=fair_price_floor,
            recommended_price=recommended_price,
            premium_price=premium_price,
            breakdown=breakdown,
        )
