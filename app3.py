import streamlit as st
import base64
from openai import OpenAI

st.set_page_config(
    layout="wide"
)


def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image

def analyze_image(image_data: str) -> str:
    prompt_instruction = """
    You are an intelligent assistant whose task is to analyze the nutrient content of a food product and determine 
    if it is a healthy option according to FSSAI standards.

    Instructions:

    **Identify the Nutrient Content:**

    -Extract the nutritional information from the food product's label.
    -List each nutrient with its quantity (e.g., calories, total fat, saturated fat, trans fat, cholesterol, sodium, total carbohydrates, dietary fiber, sugars, protein, vitamins, minerals, and any other listed nutrients).
    -Check for Potential Allergens:

    **Identify any common allergens listed in the ingredients (e.g., nuts, dairy, soy, gluten).**
    -Note the presence of these allergens.
    -Evaluate Nutritional Value:

    **Use FSSAI standards to evaluate whether the quantities of each nutrient fall within the recommended daily values or limits.**
    -Provide the FSSAI guidelines used for each nutrient.
    -Include specific limits for trans fat, cholesterol, sodium, and added sugars.
    -Assess Ingredient Sources:

    **Determine if the ingredients are natural, organic, or contain artificial additives/preservatives.**
    -Note the source of key ingredients (e.g., whole grains, natural sweeteners).
    -Evaluate Health Claims:

    **Review any health claims made on the packaging (e.g., "high in fiber," "low fat," "gluten-free").**
    -Verify if these claims are supported by the nutritional information.
    -Provide a Breakdown:

    **Detail the nutritional content for each nutrient separately.**
    -Indicate if the quantities are within healthy limits according to FSSAI standards.
    -Highlight any concerns related to allergens, artificial additives, or unsupported health claims.
    -Summarize the Results in Brief:

    **Include a brief summary of the product.**
    -Mention whether it is healthy or not based on the evaluation.
    -State any nutrients that exceed the recommended limits.
    -Note any potential allergens or artificial ingredients.
    -Provide recommendations if applicable.

    Example:

    Food Product: XYZ Granola Bar

    Nutritional Information (per serving):

    Calories: 150 kcal
    Total Fat: 5g
    Saturated Fat: 1g
    Trans Fat: 0g
    Cholesterol: 0mg
    Sodium: 120mg
    Total Carbohydrates: 22g
    Dietary Fiber: 3g
    Sugars: 10g
    Added Sugars: 5g
    Protein: 4g
    Vitamins and Minerals: Vitamin A 10%, Vitamin C 0%, Calcium 2%, Iron 4%
    Potential Allergens: Contains nuts, soy, and dairy.

    Ingredient Sources:

    Whole grains used.
    Contains natural sweeteners like honey.
    No artificial preservatives listed.
    
    Health Claims:

    "High in fiber": Supported, contains 3g of dietary fiber.
    "Low fat": Supported, contains 5g total fat.
    "Gluten-free": Not applicable, contains oats which may have gluten.
    
    Evaluation According to FSSAI Standards:

    Calories: Within the recommended limit.
    Total Fat: Within the recommended limit.
    Saturated Fat: Within the recommended limit.
    Trans Fat: Meets the recommended limit (0g).
    Cholesterol: Within the recommended limit.
    Sodium: Slightly high, should be below 100mg per serving.
    Total Carbohydrates: Within the recommended limit.
    Dietary Fiber: Meets the recommended minimum of 3g.
    Sugars: High, should be below 5g per serving.
    Added Sugars: High, consider limiting intake.
    Protein: Within the recommended limit.
    Vitamins and Minerals: Adequate.
    
    Summary:

    Product: XYZ Granola Bar
    Healthiness: Moderately healthy with some concerns.
    Total Sugars: High, limit intake to avoid excess sugar consumption.
    Sodium: Slightly high, consume in moderation.
    Allergens: Contains nuts, soy, and dairy.
    Artificial Ingredients: None listed.
    Recommendations: Consider a lower sugar and sodium alternative if available. Ensure no gluten contamination if sensitive.
    """

    client = OpenAI(api_key='')
    MODEL = "gpt-4o"

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt_instruction},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
            ]}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content

# Streamlit UI
st.sidebar.title("Food Nutrition Calculator")
uploaded_file = st.sidebar.file_uploader("Upload an image of your food order", type=["jpg", "jpeg", "png"])

if st.sidebar.button("Calculate"):
    if uploaded_file is not None:
        # Save the uploaded file
        with open("uploaded_image.png", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Encode the image
        base64_image = encode_image("uploaded_image.png")

        # Analyze the image
        result = analyze_image(base64_image)

        # Display the results
        col1, col2 = st.columns(2)
        with col1:
            st.image("uploaded_image.png", caption='Uploaded Food Order', use_column_width=True)
        with col2:
            st.markdown(result)
    else:
        st.sidebar.error("Please upload an image to proceed.")