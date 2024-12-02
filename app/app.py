import seaborn as sns                       # Provides the plot we'll use for data visualisation
from faicons import icon_svg                # Provides icons for display

from shiny import reactive                  # Provides the reactive decorator to update dashboard based on user input
from shiny.express import input, render, ui # Used by Shiny to create the dashboard
import palmerpenguins                       # Provides the dataset we'll analyze

df = palmerpenguins.load_penguins()         # Load the dataset we'll analyze

# Set the title, fillable option allows page to adapt to different screen sizes
ui.page_opts(title="Penguins dashboard", fillable=True)

# Define the sidebar layout with filter controls
with ui.sidebar(title="Filter controls"):
    # Slider input for filtering by mass
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    # Checkbox group input for selecting species
    ui.input_checkbox_group(
        "species",                                      # Name of the input to reference in the code
        "Species",                                      # Display Label
        ["Adelie", "Gentoo", "Chinstrap"],              # Options for the user to select from
        selected=["Adelie", "Gentoo", "Chinstrap"],     # These options will be checked when the app is loaded
    )
    ui.hr()                 # Horizontal rule for visual separation

    # Section for links
    ui.h6("Links")
    ui.a(
        "GitHub Source",                        # Display text for the link
        href="https://github.com/denisecase/cintel-07-tdash",   # URL to link to
        target="_blank",                    # Open the link in a new tab
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    # Link to the PyShiny documentation - a great resource for learning Shiny for Python
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )


with ui.layout_column_wrap(fill=False):
    # Value boxes create a nice graphical disply for key metrics
    with ui.value_box(showcase=icon_svg("earlybirds")):     # Uses the faicons we imported to display an icon
        "Number of penguins"

        @render.text    # Decorator that allows us to create a reactive text based on the function
        def count():
            # Return the number of rows in the filtered DataFrame
            return filtered_df().shape[0]

    # Value box to display the average bill length
    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"

        @render.text
        def bill_length():
            # Return the average (mean) bill length in mm
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    # Value box to display the average bill depth
    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            # Return the average bill depth in mm
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Layout to create columns; everything with indent after "with" will be on the top row
with ui.layout_columns():
    with ui.card(full_screen=True):    # Creates a card around the data visualisation; full_screen=True gives the user the ability to expand the card to full screen
        ui.card_header("Bill Length vs Bill Depth by Species")  # Header for the card

        # Render the plot for bill length and depth
        @render.plot
        def length_depth():
            # Create the scatter plot
            plot = sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species"
            )
            # Set the axis labels and title
            plot.set(
                xlabel = "Bill Length (mm)",
                ylabel = "Bill Depth (mm)",
            )
            # Set the legend title
            plot.legend(title="Species")
            
            return plot.figure
        
    # Another card for the summary statistics    
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")

        # Render the reactive DataFrame with summary statistics
        @render.data_frame
        def summary_statistics():
            # Define the columns to display from the dataframe
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            # Return the filtered DataFrame with selected columns
            return render.DataGrid(filtered_df()[cols], filters=True)

# Include custom CSS (if needed)
#ui.include_css(app_dir / "styles.css")

# Reactive function to filter the DataFrame based on user input
@reactive.calc
# Define the function we'll call to get the data filtered by user input
def filtered_df():
    # Uses the input values from the sidebar to filter the DataFrame
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
