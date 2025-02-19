import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set seaborn style
sns.set_theme(style="whitegrid")

def load_data(csv_filename):
    """
    Loads the all_networks_top50.csv file into a pandas DataFrame.
    Assumes the file is in the same directory as the script.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script directory
    csv_path = os.path.join(script_dir, csv_filename)  # Full path to CSV

    if not os.path.exists(csv_path):
        print(f"Error: File {csv_path} not found.")
        exit(1)
    
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    return df

def create_output_dir(folder_name):
    """Creates an output directory if it doesn't exist."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, folder_name)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def create_tables_dir():
    """Creates the 'tables' directory to save CSV tables if it doesn't exist."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tables_dir = os.path.join(script_dir, "tables")
    os.makedirs(tables_dir, exist_ok=True)
    return tables_dir

def create_top_organizations_table(df, tables_dir):
    """Creates and saves tables of top 10 organizations for each network and year."""
    print("Generating: Top 10 Organizations Table by Network and Year")

    # Group by Network and Year, then get top 10 organizations by mentions
    top_per_network_year = df.groupby(["Year", "Network", "ORG"])["Count"].sum().reset_index()
    top_per_network_year = top_per_network_year.sort_values(["Year", "Network", "Count"], ascending=[True, True, False])
    top_per_network_year = top_per_network_year.groupby(["Year", "Network"]).head(10)

    # Loop over each unique network and year and save the table
    for (year, network), group in top_per_network_year.groupby(["Year", "Network"]):
        # Save to CSV
        file_name = f"top_organizations_{network}_{year}.csv"
        output_path = os.path.join(tables_dir, file_name)
        group.to_csv(output_path, index=False)
        print(f"Table saved: {file_name}")

def plot_top_organizations(df, output_dir):
    """Plots the overall top 20 most mentioned organizations across all networks and years."""
    print("Generating: Top 20 Organizations Overall")
    plt.figure(figsize=(12, 6))
    top_orgs = df.groupby("ORG")["Count"].sum().nlargest(20)
    sns.barplot(x=top_orgs.values, y=top_orgs.index, palette="Blues_r")
    plt.xlabel("Total Mentions")
    plt.ylabel("Organization")
    plt.title("Top 20 Most Mentioned Organizations (Overall)")
    plt.savefig(os.path.join(output_dir, "top_organizations.png"))
    plt.close()

def plot_top_orgs_by_year(df, output_dir):
    """Plots the top 5 organizations for each year as a grouped bar chart."""
    print("Generating: Top 5 Organizations by Year")
    plt.figure(figsize=(14, 6))
    top_per_year = df.groupby(["Year", "ORG"])["Count"].sum().reset_index()
    top_per_year = top_per_year.sort_values(["Year", "Count"], ascending=[True, False])
    top_per_year = top_per_year.groupby("Year").head(5)

    sns.barplot(x="Year", y="Count", hue="ORG", data=top_per_year, palette="viridis")
    plt.xlabel("Year")
    plt.ylabel("Mentions")
    plt.title("Top 5 Organizations by Year")
    plt.xticks(rotation=45)
    plt.legend(title="Organization", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig(os.path.join(output_dir, "top_organizations_by_year.png"))
    plt.close()

def plot_trend_of_organizations(df, output_dir):
    """Line plot showing trends of the top 5 organizations over time."""
    print("Generating: Trends of Top 5 Organizations Over Time")
    plt.figure(figsize=(14, 6))
    top_orgs = df.groupby("ORG")["Count"].sum().nlargest(5).index
    trend_data = df[df["ORG"].isin(top_orgs)].groupby(["Year", "ORG"])["Count"].sum().reset_index()

    sns.lineplot(data=trend_data, x="Year", y="Count", hue="ORG", marker="o", palette="tab10")
    plt.xlabel("Year")
    plt.ylabel("Mentions")
    plt.title("Trends of Top 5 Organizations Over Time")
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, "organization_trends.png"))
    plt.close()

def plot_org_count_by_network(df, output_dir):
    """Stacked bar chart comparing total organization mentions by network."""
    print("Generating: Top 10 Organizations Mentioned by Network")
    plt.figure(figsize=(14, 6))
    network_counts = df.groupby(["Network", "ORG"])["Count"].sum().reset_index()
    top_orgs = df.groupby("ORG")["Count"].sum().nlargest(10).index
    network_counts = network_counts[network_counts["ORG"].isin(top_orgs)]

    sns.barplot(x="ORG", y="Count", hue="Network", data=network_counts, palette="Paired")
    plt.xlabel("Organization")
    plt.ylabel("Mentions")
    plt.title("Top 10 Organizations Mentioned by Network")
    plt.xticks(rotation=45)
    plt.legend(title="Network", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig(os.path.join(output_dir, "org_mentions_by_network.png"))
    plt.close()

def plot_distribution_of_mentions(df, output_dir):
    """Histogram showing the distribution of organization mention counts."""
    print("Generating: Distribution of Organization Mentions")
    plt.figure(figsize=(10, 5))
    sns.histplot(df["Count"], bins=30, kde=True, color="darkred")
    plt.xlabel("Mentions")
    plt.ylabel("Frequency")
    plt.title("Distribution of Organization Mentions")
    plt.savefig(os.path.join(output_dir, "distribution_mentions.png"))
    plt.close()

def plot_heatmap_presence(df, output_dir):
    """Heatmap of organization presence across years and networks."""
    print("Generating: Heatmap of Organization Presence Over Time")
    pivot_table = df.pivot_table(index="ORG", columns="Year", values="Count", aggfunc="sum").fillna(0)
    pivot_table = pivot_table.loc[pivot_table.sum(axis=1).nlargest(15).index]

    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_table, annot=True, fmt=".0f", cmap="coolwarm", linewidths=0.5)
    plt.xlabel("Year")
    plt.ylabel("Organization")
    plt.title("Organization Presence Over Time (Top 15)")
    plt.savefig(os.path.join(output_dir, "heatmap_presence.png"))
    plt.close()

def plot_top_entities_by_network_by_year(df, output_dir):
    """
    Generates histograms for the top 10 entities per year by network.
    Saves them in network_visualizations/.
    """
    print("Generating: Top 10 Entities Histograms by Network and Year")

    # Group and find top 10 per network-year
    top_per_network_year = df.groupby(["Year", "Network", "ORG"])["Count"].sum().reset_index()
    top_per_network_year = top_per_network_year.sort_values(["Year", "Network", "Count"], ascending=[True, True, False])
    top_per_network_year = top_per_network_year.groupby(["Year", "Network"]).head(10)

    # Loop over each unique network and year
    for (year, network), group in top_per_network_year.groupby(["Year", "Network"]):
        plt.figure(figsize=(10, 6))
        sns.barplot(y=group["ORG"], x=group["Count"], palette="coolwarm")
        plt.xlabel("Mentions")
        plt.ylabel("Organization")
        plt.title(f"Top 10 {network} Entities {year}")
        plt.xticks(rotation=45)
        
        # Save the figure
        file_name = f"top_10_{network}_{year}.png"
        output_path = os.path.join(output_dir, file_name)
        plt.savefig(output_path)
        plt.close()
        print(f"Saved histogram: {file_name}")

def main():
    """Main function to run all visualizations locally."""
    csv_filename = "all_networks_top50.csv"  # Change if CSV has a different name
    output_dir = create_output_dir("visualizations")
    tables_dir = create_tables_dir()
    network_viz_dir = create_output_dir("network_visualizations")
    df = load_data(csv_filename)

    create_top_organizations_table(df, tables_dir)  # Generate and save tables
    plot_top_entities_by_network_by_year(df, network_viz_dir)  # Generate and save histograms

    plot_top_organizations(df, output_dir)
    plot_top_orgs_by_year(df, output_dir)
    plot_trend_of_organizations(df, output_dir)
    plot_org_count_by_network(df, output_dir)
    plot_distribution_of_mentions(df, output_dir)
    plot_heatmap_presence(df, output_dir)

    print(f"All visualizations saved in {output_dir}")
    print(f"All tables saved in {tables_dir}")

if __name__ == "__main__":
    main()
