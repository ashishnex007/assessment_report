from flask import Flask, request, send_file
import mysql.connector
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

def generate_image(student_id):
    db_connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE")
    )

    # Create a cursor object
    cursor = db_connection.cursor()

    # Query
    query = f"SELECT std_name, dept, std_yr, section, exams, iaccuracy, caccuracy, aptitude_score, mcq_score, coding_score FROM assessment WHERE id = \"{student_id}\""

    cursor.execute(query)

    data = cursor.fetchone()

    cursor.close()
    db_connection.close()

    # Image path and font path
    image_path = "gradient.jpg"
    font_path = "Poppins-Regular.ttf"

    # Load the image
    image = Image.open(image_path)

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    # Load font
    font_size = 50
    font = ImageFont.truetype(font_path, font_size)

    # Position to start drawing text
    x = 50
    y = 50

    draw.text((250, 20), "YOUR MONTHLY ANALYTICS", font=ImageFont.truetype(font_path, 60), fill=(255, 255, 255))

    name, dept, std_yr, section, exams, iaccuracy, caccuracy, aptitude_score, mcq_score, coding_score = data

    y += 150
    draw.text((x, y), f"Name: {name}", font=ImageFont.truetype(font_path, 40), fill=(255, 255, 255))
    y += 60
    draw.text((x, y), f"Department: {dept} Year: {std_yr}  Section: {section}", font=ImageFont.truetype(font_path, 40), fill=(255, 255, 255))

    y += 150
    draw.text((x, y), f"Exams taken: {exams}", font=font, fill=(255, 255, 255))

    y += font_size + 20
    draw.text((x, y), f"Accuracy at the beginning: {iaccuracy}", font=font, fill=(255, 255, 255))
    y += font_size + 20
    draw.text((x, y), f"Accuracy now: {caccuracy}", font=font, fill=(255, 255, 255))

    y += font_size + 40
    areas_to_improve = []
    if aptitude_score < 60:
        areas_to_improve.append("Aptitude")
    if mcq_score < 60:
        areas_to_improve.append("MCQ")
    if coding_score < 60:
        areas_to_improve.append("Coding")

    if areas_to_improve:
        draw.text((x, y), f"Areas to improve: {', '.join(areas_to_improve)}", font=font, fill=(255, 255, 255))

    output_filename = f"output_{student_id}.jpg"
    image.save(output_filename)

    return output_filename

@app.route('/')
def welcome():
    return "welcome to report generation API, pls shift to \"/generate\" endpoint for report generation"

@app.route('/generate', methods=['GET'])
def api_generate_image():
    student_id = request.args.get('id')
    if not student_id:
        return "Error: Studnet not found", 400

    image_filename = generate_image(student_id)

    return send_file(image_filename, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
