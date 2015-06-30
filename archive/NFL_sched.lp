Minimize
  16 Scrap1 + 10 Scrap2 + 8 Scrap3 + 9 Scrap4 + 48 Ni + 60 Cr + 53 Mo
Subject To
 Production_Limit: Scrap1 + Scrap2 + Scrap3 + Scrap4 + Ni + Cr + Mo = 1000
 Max_Blend_C: 0.0005 Scrap1 - 0.0005 Scrap2 + 0.001 Scrap3 - 0.0035 Scrap4
   - 0.0075 Ni - 0.0075 Cr - 0.0075 Mo <= 0
 Max_Blend_Ni: 0.145 Scrap1 - 0.003 Scrap2 - 0.035 Scrap3 - 0.035 Scrap4
   + 0.965 Ni - 0.035 Cr - 0.035 Mo <= 0
 Max_Blend_Cr: 0.108 Scrap1 - 0.001 Scrap2 - 0.012 Scrap3 - 0.012 Scrap4
   - 0.012 Ni + 0.988 Cr - 0.012 Mo <= 0
 Max_Blend_Mo: - 0.013 Scrap1 - 0.012 Scrap2 - 0.013 Scrap3 - 0.013 Scrap4
   - 0.013 Ni - 0.013 Cr + 0.987 Mo <= 0
 Min_Blend_C: 0.0015 Scrap1 + 0.0005 Scrap2 + 0.002 Scrap3 - 0.0025 Scrap4
   - 0.0065 Ni - 0.0065 Cr - 0.0065 Mo >= -0
 Min_Blend_Ni: 0.15 Scrap1 + 0.002 Scrap2 - 0.03 Scrap3 - 0.03 Scrap4
   + 0.97 Ni - 0.03 Cr - 0.03 Mo >= -0
 Min_Blend_Cr: 0.11 Scrap1 + 0.001 Scrap2 - 0.01 Scrap3 - 0.01 Scrap4
   - 0.01 Ni + 0.99 Cr - 0.01 Mo >= -0
 Min_Blend_Mo: - 0.011 Scrap1 - 0.01 Scrap2 - 0.011 Scrap3 - 0.011 Scrap4
   - 0.011 Ni - 0.011 Cr + 0.989 Mo >= -0
Bounds
 Scrap1 <= 75
 Scrap2 <= 250
End
