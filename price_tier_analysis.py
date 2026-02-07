import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ───────────────────────────────────────────────
# Styling (makes charts look more professional)
# ───────────────────────────────────────────────
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("viridis")

# ───────────────────────────────────────────────
# 1. Load and prepare data
# ───────────────────────────────────────────────
df = pd.read_csv('footwear_filtered.csv')

# Price bins
bins = [0, 100, 150, 200, 250, 300, 350, 400, np.inf]
labels = ['< $100', '$100–150', '$150–200', '$200–250', 
          '$250–300', '$300–350', '$350–400', '$400+']

df['price_bin'] = pd.cut(
    df['unit_price'], 
    bins=bins, 
    labels=labels, 
    right=False, 
    include_lowest=True
)

# ───────────────────────────────────────────────
# 2. Aggregate metrics
# ───────────────────────────────────────────────
bin_stats = df.groupby('price_bin', observed=True).agg(
    orders           = ('order_id',    'count'),
    total_units      = ('quantity',    'sum'),
    avg_unit_price   = ('unit_price',  'mean'),
    total_revenue    = ('revenue',     'sum'),
    total_profit     = ('profit',      'sum')
).round(2)

bin_stats['profit_per_unit']   = (bin_stats['total_profit'] / bin_stats['total_units']).round(2)
bin_stats['margin_pct']        = (bin_stats['total_profit'] / bin_stats['total_revenue'] * 100).round(2)
bin_stats['profit_share_pct']  = (bin_stats['total_profit'] / bin_stats['total_profit'].sum() * 100).round(1)
bin_stats['revenue_share_pct'] = (bin_stats['total_revenue'] / bin_stats['total_revenue'].sum() * 100).round(1)

# Sort by total profit (most important business view)
bin_stats = bin_stats.sort_values('total_profit', ascending=False)

print("\nPrice Segment Performance Summary")
print(bin_stats)

# ───────────────────────────────────────────────
# 3. Visualizations
# ───────────────────────────────────────────────

# Figure setup - two subplots side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), gridspec_kw={'width_ratios': [5, 4]})

# ─── Left: Bar + Line - Total Profit & Profit per Unit ───
color_profit = '#2ecc71'
color_ppu    = '#e74c3c'

bars = ax1.bar(
    bin_stats.index, 
    bin_stats['total_profit'], 
    color=color_profit, 
    alpha=0.85, 
    label='Total Profit ($)'
)

ax1.set_title('Total Profit by Price Segment', fontsize=14, fontweight='bold', pad=15)
ax1.set_ylabel('Total Profit ($)', color=color_profit, fontsize=12)
ax1.tick_params(axis='y', labelcolor=color_profit)

ax1_ppu = ax1.twinx()
ax1_ppu.plot(
    bin_stats.index, 
    bin_stats['profit_per_unit'], 
    color=color_ppu, 
    marker='o', 
    linewidth=2.5, 
    markersize=8, 
    label='Profit per Unit ($)'
)
ax1_ppu.set_ylabel('Profit per Unit ($)', color=color_ppu, fontsize=12)
ax1_ppu.tick_params(axis='y', labelcolor=color_ppu)

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax1_ppu.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)

ax1.tick_params(axis='x', rotation=45, labelsize=10)
ax1.grid(True, axis='y', linestyle='--', alpha=0.7)

# ─── Right: Stacked bar - Revenue & Profit Share ───
bin_stats_sorted_rev = bin_stats.sort_values('total_revenue', ascending=True)  # for nicer stacking order

x = np.arange(len(bin_stats_sorted_rev))
width = 0.35

ax2.bar(x - width/2, bin_stats_sorted_rev['revenue_share_pct'], width, 
        label='Revenue Share %', color='#3498db', alpha=0.9)
ax2.bar(x + width/2, bin_stats_sorted_rev['profit_share_pct'], width, 
        label='Profit Share %', color='#9b59b6', alpha=0.9)

ax2.set_title('Revenue vs Profit Share by Price Segment', fontsize=14, fontweight='bold', pad=15)
ax2.set_xticks(x)
ax2.set_xticklabels(bin_stats_sorted_rev.index, rotation=45, ha='right', fontsize=10)
ax2.set_ylabel('Percentage of Total (%)', fontsize=12)
ax2.legend(loc='upper left', fontsize=10)
ax2.grid(True, axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

# ─── Optional: Extra chart - Margin stability ───
plt.figure(figsize=(10, 5))

sns.lineplot(
    x=bin_stats.index,
    y=bin_stats['margin_pct'],
    marker='o',
    linewidth=2.5,
    markersize=10,
    color='#27ae60'
)

plt.title('Gross Margin % Across Price Segments', fontsize=14, fontweight='bold', pad=15)
plt.ylabel('Gross Margin (%)', fontsize=12)
plt.xlabel('Price Segment', fontsize=12)
plt.ylim(bin_stats['margin_pct'].min() - 1, bin_stats['margin_pct'].max() + 1)
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
