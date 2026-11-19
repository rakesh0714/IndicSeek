import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


MODEL_NAME = "google/flan-t5-base"


def main():

    print("=" * 70)
    print("IndicSeek - Multilingual Generator Test")
    print("=" * 70)

    print("\nLoading FLAN-T5...")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_NAME
    )

    device = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    model = model.to(device)
    model.eval()

    print(
        f"Device: {device}"
    )

    tests = [

        {
            "language": "English",
            "question": (
                "What documents are required "
                "for a scholarship application?"
            ),
            "evidence": (
                "A scholarship application may require "
                "identity proof, academic records, "
                "bank account details, and an income "
                "certificate."
            )
        },

        {
            "language": "Hindi",
            "question": (
                "छात्रवृत्ति के लिए कौन से दस्तावेज "
                "आवश्यक हैं?"
            ),
            "evidence": (
                "छात्रवृत्ति आवेदन के लिए पहचान प्रमाण, "
                "शैक्षणिक रिकॉर्ड, बैंक खाते का विवरण "
                "और आय प्रमाण पत्र आवश्यक हो सकते हैं।"
            )
        },

        {
            "language": "Gujarati",
            "question": (
                "શિષ્યવૃત્તિ માટે કયા દસ્તાવેજો "
                "જરૂરી છે?"
            ),
            "evidence": (
                "શિષ્યવૃત્તિ અરજી માટે ઓળખનો પુરાવો, "
                "શૈક્ષણિક રેકોર્ડ, બેંક ખાતાની વિગતો "
                "અને આવકનું પ્રમાણપત્ર જરૂરી હોઈ શકે છે."
            )
        }
    ]

    for number, test in enumerate(
        tests,
        start=1
    ):

        print("\n" + "=" * 70)
        print(
            f"TEST {number}: "
            f"{test['language']}"
        )
        print("=" * 70)

        prompt = f"""
Answer the question using only the evidence.

Answer in {test['language']}.

Question:
{test['question']}

Evidence:
{test['evidence']}

Answer:
"""

        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024
        )

        inputs = {
            key: value.to(device)
            for key, value in inputs.items()
        }

        with torch.no_grad():

            output_ids = model.generate(
                **inputs,
                max_new_tokens=100,
                num_beams=4,
                do_sample=False
            )

        answer = tokenizer.decode(
            output_ids[0],
            skip_special_tokens=True
        )

        print(
            f"\nQuestion:\n"
            f"{test['question']}"
        )

        print(
            f"\nGenerated Answer:\n"
            f"{answer}"
        )

    print("\n" + "=" * 70)
    print("GENERATOR TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()