import streamlit as st
from happytransformer import HappyTextToText, TTSettings
from annotated_text import annotated_text
import difflib

checkpoint = "team-writing-assistant/t5-base-c4jfleg"


def diff_strings(a, b):
    result = []
    diff = difflib.Differ().compare(a.split(), b.split())
    replacement = ""
    for line in diff:
        if line.startswith("  "):
            if len(replacement) == 0:
                result.append(" ")
                result.append(line[2:])
            else:
                result.append(" ")
                result.append(("", replacement, "#ffd"))
                replacement = ""
                result.append(line[2:])
        elif line.startswith("- "):
            if len(replacement) == 0:
                replacement = line[2:]
            else:
                result.append(" ")
                result.append(("", replacement, "#fdd"))
                replacement = ""
        elif line.startswith("+ "):
            if len(replacement) == 0:
                result.append(("", line[2:], "#dfd"))
            else:
                result.append(" ")
                result.append((line[2:], replacement, "#ddf"))
                replacement = ""
    return result


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_happy_text(model_name):
    st.write(f"Loading the HappyTextToText model {model_name}, please wait...")
    return HappyTextToText("T5", model_name)


happy_tt = get_happy_text(checkpoint)
args = TTSettings(num_beams=5, min_length=1)

st.title("Check & Improve English Grammar")
st.markdown("This writing assistant detects 🔍 and corrects ✍️ grammatical mistakes for you!")

st.subheader("Example text: ")
col1, col2 = st.columns([1, 1])
with col1:
    example_1 = st.button("Speed of light is fastest then speed of sound")
with col2:
    example_2 = st.button("Who are the president?")

input_text = st.text_area('Enter your text here')
button = st.button('Submit')


def output(input_text):
    with st.spinner('Detecting 🔍..'):
        input_text = "grammar: " + input_text
        result = happy_tt.generate_text(input_text, args=args)
        # st.markdown("## " + result.text)
        diff = diff_strings(input_text[9:], result.text)
        annotated_text(*diff)
        

if example_1:
    output("Speed of light is fastest then speed of sound")
elif example_2:
    output("Who are the president?")
elif input_text:
    output(input_text)
  
st.text("")
st.text("Built with ❤️")
