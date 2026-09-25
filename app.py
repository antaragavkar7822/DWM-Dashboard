import streamlit as st
import matplotlib.pyplot as plt

from OLAP_Queries import prepare_olap_data


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Walmart Sales Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

data = prepare_olap_data()

df_store = data["df_store"]
df_product = data["df_product"]
df_customer = data["df_customer"]
df_sales = data["df_sales"]

total_sales = data["total_sales"]
region_sales = data["region_sales"]
monthly_sales = data["monthly_sales"]
north_monthly_sales = data["north_monthly_sales"]
dice_sales = data["dice_sales"]
pivot_sales = data["pivot_sales"]
category_sales = data["category_sales"]
brand_sales = data["brand_sales"]
store_type_sales = data["store_type_sales"]
loyalty_sales = data["loyalty_sales"]


# ============================================================
# TITLE
# ============================================================

st.title("WALMART SALES ANALYSIS DASHBOARD")
st.divider()


# ============================================================
# ROW 1
# ============================================================

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# QUERY 2 - ROLL-UP
# ------------------------------------------------------------

with col1:

    st.subheader("Query 2 • Roll-up")

    fig, ax = plt.subplots(figsize=(5, 3.2))

    ax.bar(
        region_sales.index,
        region_sales.values
    )

    ax.set_xlabel("Region")
    ax.set_ylabel("Sales")
    ax.set_title("Sales by Region")

    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)


# ------------------------------------------------------------
# QUERY 3 - DRILL-DOWN
# ------------------------------------------------------------

with col2:

    st.subheader("Query 3 • Drill-down")

    fig, ax = plt.subplots(figsize=(5, 3.2))

    ax.plot(
        monthly_sales.index,
        monthly_sales.values,
        marker="o",
        linewidth=2
    )

    ax.set_xlabel("Month")
    ax.set_ylabel("Sales")
    ax.set_title("Monthly Sales")

    ax.set_xticks(sorted(monthly_sales.index))
    ax.grid(True, alpha=0.2)

    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)


# ============================================================
# ROW 2
# ============================================================

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# QUERY 4 - SLICE
# ------------------------------------------------------------

with col1:

    st.subheader("Query 4 • Slice")

    fig, ax = plt.subplots(figsize=(5, 3.2))

    ax.plot(
        north_monthly_sales.index,
        north_monthly_sales.values,
        marker="o",
        linewidth=2
    )

    ax.set_xlabel("Month")
    ax.set_ylabel("Sales")
    ax.set_title("North Region — Monthly Sales")

    ax.set_xticks(
        sorted(north_monthly_sales.index)
    )

    ax.grid(True, alpha=0.2)

    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)


# ------------------------------------------------------------
# QUERY 5 - DICE
# ------------------------------------------------------------

with col2:

    st.subheader("Query 5 • Dice")

    fig, ax = plt.subplots(figsize=(5, 3.2))

    dice_sales.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Region")
    ax.set_ylabel("Sales")
    ax.set_title("Region × Selected Categories")

    ax.tick_params(
        axis="x",
        rotation=0
    )

    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)


# ============================================================
# ROW 3
# ============================================================

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# QUERY 6 - PIVOT
# ------------------------------------------------------------

with col1:

    st.subheader("Query 6 • Pivot")

    fig, ax = plt.subplots(figsize=(5, 3.2))

    pivot_sales.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Region")
    ax.set_ylabel("Sales")
    ax.set_title("Region × Category")

    ax.tick_params(
        axis="x",
        rotation=0
    )

    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)


# ------------------------------------------------------------
# QUERY 7 - CATEGORY
# ------------------------------------------------------------

with col2:
    
    st.subheader("Query 7 • Category")

    fig, ax = plt.subplots(figsize=(5, 2.2))

    wedges, _ = ax.pie(
        category_sales.values,
        labels=None,
        startangle=90
    )

    total = category_sales.sum()

    # Percentage labels
    import math

    for i, wedge in enumerate(wedges):

        value = category_sales.iloc[i]
        percentage = value / total * 100

        angle = (wedge.theta1 + wedge.theta2) / 2
        angle_rad = math.radians(angle)

        # --------------------------------------------------------
        # LARGE SLICES → percentage inside
        # --------------------------------------------------------

        if percentage >= 5:

            x = math.cos(angle_rad) * 0.65
            y = math.sin(angle_rad) * 0.65

            ax.text(
                x,
                y,
                f"{percentage:.1f}%",
                ha="center",
                va="center",
                fontsize=8
            )

        # --------------------------------------------------------
        # SMALL SLICES → manually left/right
        # --------------------------------------------------------

        else:

            # Pie edge
            x_start = math.cos(angle_rad)
            y_start = math.sin(angle_rad)

            # First small category → LEFT
            if i == category_sales.index.get_loc("Groceries"):

                ax.annotate(
                    f"{percentage:.1f}%",
                    xy=(x_start, y_start),
                    xytext=(-0.6, 1.1),
                    ha="right",
                    va="center",
                    fontsize=7,
                    arrowprops=dict(
                        arrowstyle="-",
                        linewidth=0.8
                    )
                )

            # Second small category → RIGHT
            elif i == category_sales.index.get_loc("Beauty"):

                ax.annotate(
                    f"{percentage:.1f}%",
                    xy=(x_start, y_start),
                    xytext=(0.6, 1.1),
                    ha="left",
                    va="center",
                    fontsize=7,
                    arrowprops=dict(
                        arrowstyle="-",
                        linewidth=0.8
                    )
                )

    # ------------------------------------------------------------
    # TITLE
    # ------------------------------------------------------------

    ax.set_title(
        "Sales by Category",
        fontsize=14
    )


    # ------------------------------------------------------------
    # CATEGORY LEGEND
    # ------------------------------------------------------------

    ax.legend(
        wedges,
        category_sales.index,
        title="Category",
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        fontsize=8,
        title_fontsize=9,
        frameon=False
    )


    # ------------------------------------------------------------
    # SAME SIZE / LEVEL AS OTHER GRAPHS
    # ------------------------------------------------------------

    # ax.set_aspect("equal")

    plt.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)


# ============================================================
# ROW 4
# ============================================================

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# QUERY 8 - BRAND
# ------------------------------------------------------------

with col1:

    st.subheader("Query 8 • Brand")

    fig, ax = plt.subplots(figsize=(5, 3.2))

    ax.barh(
        brand_sales.index,
        brand_sales.values
    )

    ax.set_xlabel("Sales")
    ax.set_ylabel("Brand")
    ax.set_title("Sales by Brand")

    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)


# ------------------------------------------------------------
# QUERY 9 - STORE TYPE
# ------------------------------------------------------------

with col2:

    st.subheader("Query 9 • Store Type")

    fig, ax = plt.subplots(figsize=(5, 3.2))

    ax.bar(
        store_type_sales.index,
        store_type_sales.values
    )

    ax.set_xlabel("Store Type")
    ax.set_ylabel("Sales")
    ax.set_title("Sales by Store Type")

    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)


# ============================================================
# ROW 5
# ============================================================

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# QUERY 10 - LOYALTY
# ------------------------------------------------------------

with col1:

    st.subheader("Query 10 • Loyalty")

    fig, ax = plt.subplots(figsize=(5, 3.2))

    labels = []

    for value in loyalty_sales.index:

        if str(value).lower() in ["true", "1"]:
            labels.append("Loyalty Members")
        else:
            labels.append("Non-Loyalty Members")

    ax.pie(
        loyalty_sales.values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Loyalty vs Non-Loyalty Sales")

    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)

