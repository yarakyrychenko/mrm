import pandas as pd, streamlit as st

data = pd.read_csv("MRM – Database of Measures.csv").fillna("Unknown")

data.columns = ["MeasureName", "MeasureAbbreviation", "CoderName", "Timestamp", "Reference", "MeasureDetails","Year","LinkPaper", "LinkMeasure",
                "Items","LengthSecs","LengthItems", "Population","Language", "Validated", "Objective", "Specific", "Online", "LongTermMalleability",
                "ShortTermMalleability", "Skill","AttitudesNormsBeliefs", "Knowledge", "BehavioralCorrelate","IdentityRiskFactor","StimuliType",
                "StimuliOrigin","StimuliSource", "StimuliCharacteristics", "StimuliPlatform", "ResponseOption", "ComponentType", "BehaviorType", "RiskType", "Comments", 
                "LinktoOriginalMeasurePaper", "KeyCorrelate", "PaperIncludeMeasure", "X"]

data.drop(columns=["X"], inplace=True)

countries = list(data.Population.unique())
countries.sort(reverse=True)
countries.insert(0, "All")

years = list(data.Year.unique())
years.sort(reverse=True)
years.insert(0, "All")

lengthitems = list(data.LengthItems.unique())
lengthitems.sort(reverse=True)
lengthitems.insert(0, "All")

language = list(data.Language.unique())
language.sort(reverse=True)
language.insert(0, "All")

validated = list(data.Validated.unique())
validated.sort(reverse=True)
validated.insert(0, "All")

objective = list(data.Objective.unique())
objective.sort(reverse=True)
objective.insert(0, "All")

specific = list(data.Specific.unique())
specific.sort(reverse=True)
specific.insert(0, "All")


st.markdown("<h1 style='text-align: center;'> Misinformation Resilience Metrics </h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'> find the measure that fits best </h3>", unsafe_allow_html=True)

def get_filtered_data(data, filtervars, vars = ["Year", "Population", "Language", "LengthItems",
                                                "Validated" , "Objective", "Specific"]):
    newdata = data.copy()
    for i in range(len(vars)):
        if len(filtervars[i]) == 0:
            pass 
        elif filtervars[i][0] == "All":
            pass
        else:
            tuplefilt = tuple(filtervars[i])
            newdata = newdata.query(f'{vars[i]} in {tuplefilt}')
    return newdata

with st.form("my_form"):
    st.markdown("Filter by:")
    
    st.multiselect("Number of Items", lengthitems, default=["All"], key="LENGTHITEMS")
    st.multiselect("Langauge", language, default=["All"], key="LANGUAGE")
    st.multiselect("Country of study", countries, default=["All"], key="COUNTRY")
    st.multiselect("Year of publication", years, default=["All"], key="YEAR")
    st.multiselect("Validated?", validated, default=["All"], key="VALIDATED")
    st.multiselect("Objective?", objective, default=["All"], key="OBJECTIVE")
    st.multiselect("Specific?", specific, default=["All"], key="SPECIFIC")

    st.form_submit_button("Submit")

if "last_filters" not in st.session_state:
    st.session_state.last_filters = []

st.session_state.filters = [st.session_state.YEAR , st.session_state.LENGTHITEMS, st.session_state.LANGUAGE, st.session_state.COUNTRY,
                            st.session_state.VALIDATED, st.session_state.OBJECTIVE, st.session_state.SPECIFIC]

st.session_state.changed = st.session_state.filters != st.session_state.last_filters

newdf = get_filtered_data(data, st.session_state.filters)

if st.session_state.changed:
    df = newdf.drop_duplicates(subset=["MeasureName"])
    df.sort_values(by=['Year'], ascending=False, inplace=True)
    if len(df.MeasureName) == 0:
        st.markdown("There are no measures matching your selection criteria.")
    else:
        st.markdown(f"There are {len(df.MeasureName)} measures matching your selection criteria.")
        i = 0
        for MeasureName in pd.unique(df.MeasureName):
            i += 1
            st.markdown(f"{i}. {df[df.MeasureName==MeasureName].Year}. {df[df.MeasureName==MeasureName].MeasureName}. Link to Paper: {df[df.MeasureName==MeasureName].LinkPaper}. Link to Measure: {df[df.MeasureName==MeasureName].LinkMeasure}") 

    st.session_state.last_filters = st.session_state.filters
    st.session_state.df = df.reset_index(inplace=False)
