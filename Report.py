import streamlit as st
from pymongo import MongoClient
import logging
import uuid
import base64
from io import BytesIO
# import onedrivesdk
# This library is deprecated, consider using an alternative library for working with OneDrive
# from onedrivesdk.helpers import GetAuthCodeServer
import requests
from streamlit_option_menu import option_menu

# Set page configuration at the start
# st.set_page_config(page_title="Dashboard", page_icon="🌍", layout="wide")

# Configure logging
logging.basicConfig(level=logging.INFO)

@st.cache_data  # Updated from st.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("image.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://images.unsplash.com/photo-1501426026826-31c667bdf23d");
background-size: 300%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# MongoDB connection
try:
    client = MongoClient(r"mongodb://urbsdbsyestem:0yKSD1jkhHHka0b8rW4LfOcz31wLDfNiwRF8VIF82WHYWj3MeEHyqXDqcgWmNWiqBoDAwW85u1ZOACDbE8vu5g==@urbsdbsyestem.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@urbsdbsyestem@")
    db = client['urbs_project']
    logging.info("Connected to MongoDB successfully.")
except Exception as e:
    logging.error(f"Error connecting to MongoDB: {e}")


def project_view():
    st.markdown("<h1 style='text-align: center;'>PROJECT VIEW</h1>",
                unsafe_allow_html=True)

    # Create a selection box for the project type
    project_type = st.radio("Choose an option:",
                            ("Existing Case", "Propose System"))
    collection_name = 'baseline_model' if project_type == 'Existing Case' else 'proposed_model'

    # Fetch unique project names from the selected collection
    project_names = []
    try:
        collection = db[collection_name]
        project_names = collection.distinct("project_name")
    except Exception as e:
        st.error(f"Error fetching project names: {e}")
        logging.error(f"Error fetching project names: {e}")

    # Select box for project names
    selected_project = st.selectbox("Select Project Name", project_names)

    if selected_project:
        # Fetch and display data for the selected project
        try:
            project = collection.find_one({"project_name": selected_project})
            if project:
                # Create containers for the cards
                with st.container():
                    st.markdown(
                        f"""
                        <div class="magic-card" style="border: 2px solid black; padding: 10px; margin: 10px;">
                            <h2 style='text-align: center; color: red;'>{project.get("project_name", "N/A")}</h2>
                            <h3 style='text-align: center;'>Total Area: {project.get("total_area", "N/A")} {project.get("area_unit", "N/A")}</h3>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with st.container():
                    electricity_consumption = project.get("electricity_consumption", "N/A")
                    gas_consumption = project.get("gas_consumption", "N/A")
                    steam_energy_consumption = project.get("steam_energy_consumption", "N/A")
                    total_energy_consumption = project.get("total_energy_consumption", "N/A")
                    electricity_energy_cost = project.get("electricity_energy_cost", "N/A")
                    gas_energy_cost = project.get("gas_energy_cost", "N/A")
                    steam_energy_cost = project.get("steam_energy_cost", "N/A")
                    total_energy_cost = project.get("total_energy_cost", "N/A")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(
                            f"""
                            <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                                <div class="metric-label">Electricity Consumption (kWh)</div>
                                <div class="metric-count">{electricity_consumption}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f"""
                            <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                                <div class="metric-label">Gas Consumption (kWh)</div>
                                <div class="metric-count">{gas_consumption}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f"""
                            <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                                <div class="metric-label">Steam Energy Consumption (kWh)</div>
                                <div class="metric-count">{steam_energy_consumption}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f"""
                            <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                                <div class="metric-label">Total Energy Consumption (kWh)</div>
                                <div class="metric-count">{total_energy_consumption}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with col2:
                        st.markdown(
                            f"""
                            <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                                <div class="metric-label">Electricity Energy Cost</div>
                                <div class="metric-count">{electricity_energy_cost}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f"""
                            <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                                <div class="metric-label">Gas Energy Cost</div>
                                <div class="metric-count">{gas_energy_cost}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f"""
                            <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                                <div class="metric-label">Steam Energy Cost</div>
                                <div class="metric-count">{steam_energy_cost}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f"""
                            <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                                <div class="metric-label">Total Energy Cost</div>
                                <div class="metric-count">{total_energy_cost}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                with st.container():
                    eui_kwh_m2 = project.get("eui_kwh_m2", "N/A")
                    eui_kbtu_ft2 = project.get("eui_kbtu_ft2", "N/A")
                    total_carbon_emission = project.get(
                        "total_carbon_emission", "N/A")

                    st.markdown(
                        f"""
                        <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                            <div class="metric-label">EUI (kWh/m²)</div>
                            <div class="metric-count">{eui_kwh_m2}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"""
                        <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                            <div class="metric-label">EUI (kBtu/ft²)</div>
                            <div class="metric-count">{eui_kbtu_ft2}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"""
                        <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                            <div class="metric-label">Total Carbon Emission (tCO2)</div>
                            <div class="metric-count">{total_carbon_emission}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with st.container():
                    uvalue = project.get("uvalue", "N/A")
                    external_wall1_uvalue = project.get("external_wall1_uvalue", "N/A")
                    external_wall2_uvalue = project.get("external_wall2_uvalue", "N/A")
                    external_wall3_uvalue = project.get("external_wall3_uvalue", "N/A")
                    external_wall4_uvalue = project.get("external_wall4_uvalue", "N/A")
                    glass_uvalue = project.get("glass_uvalue", "N/A")
                    shgc = project.get("shgc", "N/A")
                    thermal_mass_building = project.get("thermal_mass_building", "N/A")
                    infiltration = project.get("infiltration", "N/A")
                    outdoor_air_summer_temp = project.get("outdoor_air_summer_temp", "N/A")
                    outdoor_air_winter_temp = project.get("outdoor_air_winter_temp", "N/A")
                    dbt = project.get("dbt", "N/A")
                    wbt = project.get("wbt", "N/A")

                    col1, col2 = st.columns(2)  # Create two columns

                    with col1:
                        st.markdown(f"""
                        <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                            <div class="metric-label">Uvalue</div>
                            <div class="metric-count">{uvalue}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"""
                        <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                            <div class="metric-label">External Wall 1 Uvalue</div>
                            <div class="metric-count">{external_wall1_uvalue}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"""
                        <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                            <div class="metric-label">External Wall 2 Uvalue</div>
                            <div class="metric-count">{external_wall2_uvalue}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"""
                        <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                            <div class="metric-label">Glass Uvalue</div>
                            <div class="metric-count">{glass_uvalue}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"""
                        <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                            <div class="metric-label">SHGC</div>
                            <div class="metric-count">{shgc}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"""
                        <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                            <div class="metric-label">Outdoor Air Winter Temperature (°C)</div>
                            <div class="metric-count">{outdoor_air_winter_temp}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"""
                        <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                            <div class="metric-label">DBT (°C)</div>
                            <div class="metric-count">{dbt}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"""
                        <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                            <div class="metric-label">WBT (°C)</div>
                            <div class="metric-count">{wbt}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.markdown(f"""
                        <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                            <div class="metric-label">External Wall 3 Uvalue</div>
                            <div class="metric-count">{external_wall3_uvalue}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"""
                        <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                            <div class="metric-label">External Wall 4 Uvalue</div>
                            <div class="metric-count">{external_wall4_uvalue}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"""
                        <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                            <div class="metric-label">Thermal Mass of Building</div>
                            <div class="metric-count">{thermal_mass_building}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"""
                        <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                            <div class="metric-label">Infiltration</div>
                            <div class="metric-count">{infiltration}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"""
                        <div class="metric-card" style="border: 2px solid black; padding: 10px;">
                            <div class="metric-label">Outdoor Air Summer Temperature (°C)</div>
                            <div class="metric-count">{outdoor_air_summer_temp}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    

                # Add Edit button
                if st.button("Edit"):
                    with st.form(key='edit_project_form'):
                        # Pre-fill input fields with current project data
                        project_name = st.text_input(
                            "Project Name", value=project.get("project_name", ""))
                        total_area = st.number_input("Total Area", value=float(
                            project.get("total_area", 0)), min_value=0.0, format="%.2f")
                        area_unit = st.selectbox("Area Unit", ["Square Meters", "Square Feet"], index=0 if project.get(
                            "area_unit") == "Square Meters" else 1)
                        electricity_consumption = st.number_input("Electricity Consumption (kWh)", value=float(
                            project.get("electricity_consumption", 0)), min_value=0.0, format="%.2f")
                        gas_consumption = st.number_input("Gas Consumption (kWh)", value=float(
                            project.get("gas_consumption", 0)), min_value=0.0, format="%.2f")
                        steam_energy_consumption = st.number_input("Steam Energy Consumption (kWh)", value=float(
                            project.get("steam_energy_consumption", 0)), min_value=0.0, format="%.2f")
                        electricity_energy_cost = st.number_input("Electricity Energy Cost", value=float(
                            project.get("electricity_energy_cost", 0)), min_value=0.0, format="%.2f")
                        gas_energy_cost = st.number_input("Gas Energy Cost", value=float(
                            project.get("gas_energy_cost", 0)), min_value=0.0, format="%.2f")
                        steam_energy_cost = st.number_input("Steam Energy Cost", value=float(
                            project.get("steam_energy_cost", 0)), min_value=0.0, format="%.2f")
                        uvalue = st.number_input("Uvalue", value=float(
                            project.get("uvalue", 0)), min_value=0.0, format="%.2f")
                        external_wall1_uvalue = st.number_input("External Wall 1 Uvalue", value=float(
                            project.get("external_wall1_uvalue", 0)), min_value=0.0, format="%.2f")
                        external_wall2_uvalue = st.number_input("External Wall 2 Uvalue", value=float(
                            project.get("external_wall2_uvalue", 0)), min_value=0.0, format="%.2f")
                        external_wall3_uvalue = st.number_input("External Wall 3 Uvalue", value=float(
                            project.get("external_wall3_uvalue", 0)), min_value=0.0, format="%.2f")
                        external_wall4_uvalue = st.number_input("External Wall 4 Uvalue", value=float(
                            project.get("external_wall4_uvalue", 0)), min_value=0.0, format="%.2f")
                        glass_uvalue = st.number_input("Glass Uvalue", value=float(
                            project.get("glass_uvalue", 0)), min_value=0.0, format="%.2f")
                        shgc = st.number_input("SHGC", value=float(
                            project.get("shgc", 0)), min_value=0.0, format="%.2f")
                        thermal_mass_building = st.number_input("Thermal Mass of Building", value=float(
                            project.get("thermal_mass_building", 0)), min_value=0.0, format="%.2f")
                        infiltration = st.number_input("Infiltration", value=float(
                            project.get("infiltration", 0)), min_value=0.0, format="%.2f")
                        outdoor_air_summer_temp = st.number_input("Outdoor Air Summer Temperature (°C)", value=float(
                            project.get("outdoor_air_summer_temp", 0)), min_value=0.0, format="%.2f")
                        outdoor_air_winter_temp = st.number_input("Outdoor Air Winter Temperature (°C)", value=float(
                            project.get("outdoor_air_winter_temp", 0)), min_value=0.0, format="%.2f")
                        dbt = st.number_input("DBT (°C)", value=float(
                            project.get("dbt", 0)), min_value=0.0, format="%.2f")
                        wbt = st.number_input("WBT (°C)", value=float(
                            project.get("wbt", 0)), min_value=0.0, format="%.2f")

                        submit_button = st.form_submit_button(
                            label='Update Project')

                        if submit_button:
                            # Prepare updated project data
                            updated_project_data = {
                                "project_name": project_name,
                                "total_area": f"{total_area:.2f}",
                                "area_unit": area_unit,
                                "electricity_consumption": f"{electricity_consumption:.2f}",
                                "gas_consumption": f"{gas_consumption:.2f}",
                                "steam_energy_consumption": f"{steam_energy_consumption:.2f}",
                                "electricity_energy_cost": f"{electricity_energy_cost:.2f}",
                                "gas_energy_cost": f"{gas_energy_cost:.2f}",
                                "steam_energy_cost": f"{steam_energy_cost:.2f}",
                                "uvalue": f"{uvalue:.2f}",
                                "external_wall1_uvalue": f"{external_wall1_uvalue:.2f}",
                                "external_wall2_uvalue": f"{external_wall2_uvalue:.2f}",
                                "external_wall3_uvalue": f"{external_wall3_uvalue:.2f}",
                                "external_wall4_uvalue": f"{external_wall4_uvalue:.2f}",
                                "glass_uvalue": f"{glass_uvalue:.2f}",
                                "shgc": f"{shgc:.2f}",
                                "thermal_mass_building": f"{thermal_mass_building:.2f}",
                                "infiltration": f"{infiltration:.2f}",
                                "outdoor_air_summer_temp": f"{outdoor_air_summer_temp:.2f}",
                                "outdoor_air_winter_temp": f"{outdoor_air_winter_temp:.2f}",
                                "dbt": f"{dbt:.2f}",
                                "wbt": f"{wbt:.2f}",
                            }

                            # Update the database
                            try:
                                collection.update_one(
                                    {"project_name": selected_project},  # Filter
                                    {"$set": updated_project_data}       # Update
                                )
                                st.success(
                                    "Project data has been successfully updated.")
                                logging.info(
                                    "Project data has been successfully updated.")
                                
                                # Update selected_project to reflect changes
                                selected_project = project_name  # Update the selected project
                            except Exception as e:
                                st.error(
                                    f"An error occurred while updating data: {e}")
                                logging.error(
                                    f"An error occurred while updating data: {e}")

        except Exception as e:
            st.error(f"Error fetching project data: {e}")
            logging.error(f"Error fetching project data: {e}")


def add_project():
    st.markdown("<h1 style='text-align: center;'>New Project</h1>",
                unsafe_allow_html=True)

    # Create a selection box for the project type
    project_type = st.radio("Choose an option:",
                            ("Existing Case", "Propose System"))
    collection_name = 'baseline_model' if project_type == 'Existing Case' else 'proposed_model'

    with st.form(key='project_form'):
        project_name = st.text_input("Project Name")
        total_area = st.number_input(
            "Total Area", min_value=0.0, format="%.2f")
        area_unit = st.selectbox("Area Unit", ["Square Meters", "Square Feet"])
        electricity_consumption = st.number_input(
            "Electricity Consumption (kWh)", min_value=0.0, format="%.2f")
        gas_consumption = st.number_input(
            "Gas Consumption (kWh)", min_value=0.0, format="%.2f")
        steam_energy_consumption = st.number_input(
            "Steam Energy Consumption (kWh)", min_value=0.0, format="%.2f")

        currency = st.selectbox("Currency", ["$", "₹"])
        electricity_energy_cost = st.number_input(
            f"Electricity Energy Cost ({currency})", min_value=0.0, format="%.2f")
        gas_energy_cost = st.number_input(
            f"Gas Energy Cost ({currency})", min_value=0.0, format="%.2f")
        steam_energy_cost = st.number_input(
            f"Steam Energy Cost ({currency})", min_value=0.0, format="%.2f")

        uvalue = st.number_input("Uvalue", min_value=0.0, format="%.2f")
        external_wall1_uvalue = st.number_input(
            "External Wall 1 Uvalue", min_value=0.0, format="%.2f")
        external_wall2_uvalue = st.number_input(
            "External Wall 2 Uvalue", min_value=0.0, format="%.2f")
        external_wall3_uvalue = st.number_input(
            "External Wall 3 Uvalue", min_value=0.0, format="%.2f")
        external_wall4_uvalue = st.number_input(
            "External Wall 4 Uvalue", min_value=0.0, format="%.2f")
        glass_uvalue = st.number_input(
            "Glass Uvalue", min_value=0.0, format="%.2f")
        shgc = st.number_input("SHGC", min_value=0.0, format="%.2f")
        thermal_mass_building = st.number_input(
            "Thermal Mass of Building", min_value=0.0, format="%.2f")
        infiltration = st.number_input(
            "Infiltration", min_value=0.0, format="%.2f")
        outdoor_air_summer_temp = st.number_input(
            "Outdoor Air Summer Temperature (°C)", min_value=0.0, format="%.2f")
        outdoor_air_winter_temp = st.number_input(
            "Outdoor Air Winter Temperature (°C)", min_value=0.0, format="%.2f")
        dbt = st.number_input("DBT (°C)", min_value=0.0, format="%.2f")
        wbt = st.number_input("WBT (°C)", min_value=0.0, format="%.2f")

        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            total_energy_consumption = electricity_consumption + \
                gas_consumption + steam_energy_consumption
            total_energy_cost = (
                electricity_consumption * electricity_energy_cost) + (gas_consumption * gas_energy_cost) + (steam_energy_consumption * steam_energy_cost)

            if total_area == 0:
                st.error("Total Area cannot be zero.")
                return

            if area_unit == "Square Feet":
                total_area_m2 = total_area / 10.76
                eui_kwh_m2 = total_energy_consumption / total_area_m2
                eui_kbtu_ft2 = eui_kwh_m2 * 0.317
                st.write("Total Area in Square Meters:", total_area_m2)
            else:
                total_area_ft2 = total_area * 10.76
                eui_kwh_m2 = total_energy_consumption / total_area
                eui_kbtu_ft2 = eui_kwh_m2 * 0.317
                st.write("Total Area in Square Feet:", total_area_ft2)

            # Emission factors
            emission_factor_electricity_kwh = 0.00028896
            emission_factor_gas_kwh = 0.000181219

            # Calculate carbon emissions
            carbon_emission_electricity = electricity_consumption * \
                emission_factor_electricity_kwh
            carbon_emission_gas = gas_consumption * emission_factor_gas_kwh
            total_carbon_emission = carbon_emission_electricity + carbon_emission_gas

            st.write("Project Name:", project_name)
            st.write("Total Area:", total_area, area_unit)
            st.write("Electricity Consumption (kWh):", electricity_consumption)
            st.write("Gas Consumption (kWh):", gas_consumption)
            st.write("Steam Energy Consumption (kWh):",
                     steam_energy_consumption)
            st.write("Total Energy Consumption (kWh):",
                     total_energy_consumption)
            st.write("Electricity Energy Cost:", electricity_energy_cost)
            st.write("Gas Energy Cost:", gas_energy_cost)
            st.write("Steam Energy Cost:", steam_energy_cost)
            st.write("Total Energy Cost:", total_energy_cost)
            st.write("Uvalue:", uvalue)
            st.write("External Wall 1 Uvalue:", external_wall1_uvalue)
            st.write("External Wall 2 Uvalue:", external_wall2_uvalue)
            st.write("External Wall 3 Uvalue:", external_wall3_uvalue)
            st.write("External Wall 4 Uvalue:", external_wall4_uvalue)
            st.write("Glass Uvalue:", glass_uvalue)
            st.write("SHGC:", shgc)
            st.write("Thermal Mass of Building:", thermal_mass_building)
            st.write("Infiltration:", infiltration)
            st.write("Outdoor Air Summer Temperature (°C):",
                     outdoor_air_summer_temp)
            st.write("Outdoor Air Winter Temperature (°C):",
                     outdoor_air_winter_temp)
            st.write("DBT (°C):", dbt)
            st.write("WBT (°C):", wbt)
            st.write("EUI (kWh/m²):", eui_kwh_m2)
            st.write("EUI (kBtu/ft²):", eui_kbtu_ft2)
            st.write("Total Carbon Emission (tCO2):", total_carbon_emission)

            # Generate unique IDs
            unique_id = str(uuid.uuid4())
            shard_key = f"{project_name}_{unique_id}"

            # Store data in MongoDB
            project_data = {
                "project_name": project_name,
                "total_area": f"{total_area:.2f}",
                "area_unit": area_unit,
                "electricity_consumption": f"{electricity_consumption:.2f}",
                "gas_consumption": f"{gas_consumption:.2f}",
                "steam_energy_consumption": f"{steam_energy_consumption:.2f}",
                "currency": currency,
                "electricity_energy_cost": f"{electricity_energy_cost:.2f}",
                "gas_energy_cost": f"{gas_energy_cost:.2f}",
                "steam_energy_cost": f"{steam_energy_cost:.2f}",
                "uvalue": f"{uvalue:.2f}",
                "external_wall1_uvalue": f"{external_wall1_uvalue:.2f}",
                "external_wall2_uvalue": f"{external_wall2_uvalue:.2f}",
                "external_wall3_uvalue": f"{external_wall3_uvalue:.2f}",
                "external_wall4_uvalue": f"{external_wall4_uvalue:.2f}",
                "glass_uvalue": f"{glass_uvalue:.2f}",
                "shgc": f"{shgc:.2f}",
                "thermal_mass_building": f"{thermal_mass_building:.2f}",
                "infiltration": f"{infiltration:.2f}",
                "outdoor_air_summer_temp": f"{outdoor_air_summer_temp:.2f}",
                "outdoor_air_winter_temp": f"{outdoor_air_winter_temp:.2f}",
                "dbt": f"{dbt:.2f}",
                "wbt": f"{wbt:.2f}",
                "total_energy_consumption": f"{total_energy_consumption:.2f}",
                "total_energy_cost": f"{total_energy_cost:.2f}",
                "eui_kwh_m2": f"{eui_kwh_m2:.2f}",
                "eui_kbtu_ft2": f"{eui_kbtu_ft2:.2f}",
                "total_carbon_emission": f"{total_carbon_emission:.2f}",
                "baselineid": shard_key if project_type == 'Existing Case' else None,
                "proposedid": shard_key if project_type == 'Propose System' else None
            }

            try:
                logging.info(
                    f"Attempting to insert/update data in collection: {collection_name}")
                collection = db[collection_name]
                collection.update_one(
                    {"project_name": project_name},  # Filter
                    {"$set": project_data},          # Update
                    upsert=True                      # Insert if not found
                )
                st.success(
                    "Project data has been successfully saved to the database.")
                logging.info(
                    "Project data has been successfully saved to the database.")
            except Exception as e:
                st.error(
                    f"An error occurred while saving data to the database: {e}")
                logging.error(
                    f"An error occurred while saving data to the database: {e}")


def report_view():
    st.markdown("<h1 style='text-align: center;'>Report View</h1>",
                unsafe_allow_html=True)

    folder_link = "https://urbssystems-my.sharepoint.com/:f:/g/personal/akash_yadav_urbs_systems/EpFUMX61HwdOrB2OKmlLNlsB8E0wFznE7YJHrSDwLo_H2w?e=sQbaJ0"
    st.markdown(f"[Shared Folder Link]({folder_link})", unsafe_allow_html=True)

    # Fetch the folder contents
    try:
        response = requests.get(folder_link)
        response.raise_for_status()

        # Check if the response is JSON
        if 'application/json' in response.headers['Content-Type']:
            files = response.json()  # Adjust this line based on actual response format

            for file in files:
                if file['name'].endswith('.xlsx'):
                    # Adjust based on actual response structure
                    file_link = file['link']
                    st.markdown(f"[{file['name']}]({file_link})",
                                unsafe_allow_html=True)
        else:
            # Log the response content for debugging
            logging.error(
                "Response is not in JSON format. Response content: %s", response.text)
            st.error("Response is not in JSON format. Attempting to parse HTML.")

            # Handle HTML response (you may need BeautifulSoup or similar)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find all anchor tags
            files = soup.find_all('a')  # Adjust based on actual HTML structure

            # Extract links to Excel files
            for file in files:
                href = file.get('href', '')
                if href.endswith('.xlsx'):
                    file_name = file.text.strip()  # Get the file name
                    # Ensure the link is absolute
                    if not href.startswith('http'):
                        href = folder_link + href  # Adjust this based on how the link is structured
                    st.markdown(f"[{file_name}]({href})",
                                unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error loading report: {e}")
        logging.error(f"Error loading report: {e}")
        
        
def contact_us():
    st.header(":mailbox: Get In Touch With Me!")

    contact_form = """
    <form action="https://formsubmit.co/akash.yadav@urbs.systems" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here"></textarea>
        <button type="submit">Send</button>
    </form>
    """

    st.markdown(contact_form, unsafe_allow_html=True)

   


def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def sideBar():
    with st.sidebar:
        # Insert logo at the top of the sidebar
        st.image(r"urbs+logo+narrow+(transparent).png",
                 width=350)  # Update the path to your logo
        selected = option_menu(
            menu_title="Main Menu",  # Added menu title
            options=["Report View", "Project View", "New Project", "Contact Us"],
            icons=["speedometer2", "file-earmark-text", "plus", "envelope", "envelope-fill"],
            menu_icon="cast",
            default_index=0
        )

    # Add CSS for responsive sidebar
    st.markdown(
        """
        <style>
            .stSidebar {
                padding: 10px;  /* Add padding */
                width: auto;  /* Allow width to adjust automatically */
                max-width: 300px;  /* Set a max width */
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    if selected == "Project View":
        project_view()
    elif selected == "New Project":
        add_project()
    elif selected == "Report View":
        report_view()
    elif selected == "Contact Us":
        contact_us()
    st.sidebar.markdown('<div style="position: absolute; top: 10px; left: 50%; transform: translateX(-50%);">'
                        '<form method="get" action="https://urbs.systems/">'
                        '<button type="submit" style="background-color: transparent; border-color: black; cursor: pointer;font-size: larger;">'
                        '<span style="font-weight: bold;">Logout</span>'
                        '</button>'
                        '</form>'
                        '</div>', unsafe_allow_html=True)


def main() -> object:
    # if authenticate():
    st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        .icon.bi-cast {
            visibility: hidden;
            display: none;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        #stDecoration {display:none;}
    </style>
    """, unsafe_allow_html=True)

    # load Style css
    css_file_path = r'style.css'
    try:
        with open(css_file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {css_file_path}")
        logging.error(f"CSS file not found: {css_file_path}")

    sideBar()


if __name__ == '__main__':
    main()
