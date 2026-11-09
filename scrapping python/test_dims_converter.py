def format_dims_4_units(length_in, width_in, height_in, radius_in=None):
    # 1. Inches
    in_str = f"{length_in:.1f}\" × {width_in:.1f}\" × {height_in:.1f}\""
    if radius_in is not None:
        in_str += f" (R: {radius_in:.1f}\")"
        
    # 2. Feet and inches
    def to_ft_in(val):
        feet = int(val // 12)
        inches = round(val % 12)
        if inches == 12:
            feet += 1
            inches = 0
        return f"{feet}'{inches}\""
    
    ft_str = f"{to_ft_in(length_in)} × {to_ft_in(width_in)} × {to_ft_in(height_in)}"
    if radius_in is not None:
        ft_str += f" (R: {to_ft_in(radius_in)})"
        
    # 3. Centimeters
    cm_l = round(length_in * 2.54, 1)
    cm_w = round(width_in * 2.54, 1)
    cm_h = round(height_in * 2.54, 1)
    cm_str = f"{cm_l} × {cm_w} × {cm_h} cm"
    if radius_in is not None:
        cm_r = round(radius_in * 2.54, 1)
        cm_str += f" (R: {cm_r} cm)"
        
    # 4. Millimeters
    mm_l = round(length_in * 25.4)
    mm_w = round(width_in * 25.4)
    mm_h = round(height_in * 25.4)
    mm_str = f"{mm_l} × {mm_w} × {mm_h} mm"
    if radius_in is not None:
        mm_r = round(radius_in * 25.4)
        mm_str += f" (R: {mm_r} mm)"
        
    return {
        "in": in_str,
        "ft": ft_str,
        "cm": cm_str,
        "mm": mm_str
    }

# Test on Glow: 84 x 76 x 33, R=8
glow_dims = format_dims_4_units(84.0, 76.0, 33.0, 8.0)
print("GLOW 4 Units:")
for k, v in glow_dims.items():
    print(f"  {k:3}: {v}")

# Test on Grandee: 100 x 91 x 38, R=8
grandee_dims = format_dims_4_units(100.0, 91.0, 38.0, 8.0)
print("\nGRANDEE 4 Units:")
for k, v in grandee_dims.items():
    print(f"  {k:3}: {v}")
