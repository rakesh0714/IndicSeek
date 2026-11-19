import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DOCUMENT_DIR = PROJECT_ROOT / "data" / "dev_documents"
QUERY_FILE = PROJECT_ROOT / "data" / "dev_queries.json"


# ============================================================
# DOCUMENT DATA
# ============================================================

documents = [
    # --------------------------------------------------------
    # SCHOLARSHIPS: 001-015
    # --------------------------------------------------------

    {
        "id": "d001",
        "category": "scholarship",
        "title": "Scholarship Eligibility",
        "text": """
English:
Undergraduate students may apply for scholarship assistance. Eligibility can depend on academic performance, family income, category, and the specific conditions of the scholarship scheme.

Hindi:
स्नातक विद्यार्थी छात्रवृत्ति सहायता के लिए आवेदन कर सकते हैं। पात्रता शैक्षणिक प्रदर्शन, पारिवारिक आय, श्रेणी और छात्रवृत्ति योजना की विशेष शर्तों पर निर्भर कर सकती है।

Gujarati:
સ્નાતક વિદ્યાર્થીઓ શિષ્યવૃત્તિ સહાય માટે અરજી કરી શકે છે. પાત્રતા શૈક્ષણિક પ્રદર્શન, પરિવારની આવક, વર્ગ અને શિષ્યવૃત્તિ યોજનાની ચોક્કસ શરતો પર આધારિત હોઈ શકે છે.
"""
    },

    {
        "id": "d002",
        "category": "scholarship",
        "title": "Scholarship Application Documents",
        "text": """
English:
A scholarship application may require identity proof, academic records, bank account details, and an income certificate. Applicants should check the scheme-specific document list before submission.

Hindi:
छात्रवृत्ति आवेदन में पहचान प्रमाण, शैक्षणिक रिकॉर्ड, बैंक खाते का विवरण और आय प्रमाण पत्र की आवश्यकता हो सकती है। आवेदन से पहले योजना की दस्तावेज सूची जांचनी चाहिए।

Gujarati:
શિષ્યવૃત્તિ અરજી માટે ઓળખનો પુરાવો, શૈક્ષણિક રેકોર્ડ, બેંક ખાતાની વિગતો અને આવક પ્રમાણપત્ર જરૂરી હોઈ શકે છે. અરજી કરતા પહેલાં યોજનાની દસ્તાવેજોની યાદી તપાસવી જોઈએ.
"""
    },

    {
        "id": "d003",
        "category": "scholarship",
        "title": "Merit Scholarship",
        "text": """
English:
Merit scholarships are generally awarded on the basis of academic achievement. Previous examination marks, grades, and continued academic performance may be considered.

Hindi:
मेधावी छात्रवृत्तियां सामान्यतः शैक्षणिक उपलब्धि के आधार पर दी जाती हैं। पिछली परीक्षा के अंक, ग्रेड और निरंतर शैक्षणिक प्रदर्शन पर विचार किया जा सकता है।

Gujarati:
મેરિટ શિષ્યવૃત્તિ સામાન્ય રીતે શૈક્ષણિક સિદ્ધિના આધારે આપવામાં આવે છે. અગાઉની પરીક્ષાના ગુણ, ગ્રેડ અને સતત શૈક્ષણિક પ્રદર્શન ધ્યાનમાં લેવામાં આવી શકે છે.
"""
    },

    {
        "id": "d004",
        "category": "scholarship",
        "title": "Income Based Scholarship",
        "text": """
English:
Some scholarship schemes provide financial support to students from economically weaker families. Family income must normally remain within the income limit defined by the scheme.

Hindi:
कुछ छात्रवृत्ति योजनाएं आर्थिक रूप से कमजोर परिवारों के विद्यार्थियों को वित्तीय सहायता प्रदान करती हैं। पारिवारिक आय योजना द्वारा निर्धारित सीमा के भीतर होनी चाहिए।

Gujarati:
કેટલીક શિષ્યવૃત્તિ યોજનાઓ આર્થિક રીતે નબળા પરિવારોના વિદ્યાર્થીઓને નાણાકીય સહાય આપે છે. પરિવારની આવક યોજનામાં નક્કી કરેલી મર્યાદામાં હોવી જરૂરી છે.
"""
    },

    {
        "id": "d005",
        "category": "scholarship",
        "title": "Government Scholarship Portal",
        "text": """
English:
Students applying for government scholarships should use the designated scholarship portal. Registration normally requires personal information and supporting academic and financial documents.

Hindi:
सरकारी छात्रवृत्ति के लिए विद्यार्थियों को निर्धारित छात्रवृत्ति पोर्टल का उपयोग करना चाहिए। पंजीकरण में व्यक्तिगत जानकारी तथा शैक्षणिक और वित्तीय दस्तावेज मांगे जा सकते हैं।

Gujarati:
સરકારી શિષ્યવૃત્તિ માટે વિદ્યાર્થીઓએ નિર્ધારિત શિષ્યવૃત્તિ પોર્ટલનો ઉપયોગ કરવો જોઈએ. નોંધણી માટે વ્યક્તિગત માહિતી તેમજ શૈક્ષણિક અને નાણાકીય દસ્તાવેજો જરૂરી હોઈ શકે છે.
"""
    },

    {
        "id": "d006",
        "category": "scholarship",
        "title": "Scholarship Renewal",
        "text": """
English:
Scholarship renewal may require students to maintain academic performance and submit a renewal application before the deadline. Previous scholarship recipients should verify the renewal conditions.

Hindi:
छात्रवृत्ति नवीनीकरण के लिए विद्यार्थियों को शैक्षणिक प्रदर्शन बनाए रखना और समय सीमा से पहले नवीनीकरण आवेदन जमा करना पड़ सकता है। पुराने लाभार्थियों को नवीनीकरण की शर्तें जांचनी चाहिए।

Gujarati:
શિષ્યવૃત્તિ નવીકરણ માટે વિદ્યાર્થીઓએ શૈક્ષણિક પ્રદર્શન જાળવવું અને સમયમર્યાદા પહેલાં નવીકરણ અરજી કરવી પડી શકે છે. અગાઉના લાભાર્થીઓએ નવીકરણની શરતો તપાસવી જોઈએ.
"""
    },

    {
        "id": "d007",
        "category": "scholarship",
        "title": "Scholarship Deadline",
        "text": """
English:
Scholarship applications must be submitted before the announced deadline. Late applications may not be considered, so students should complete document verification early.

Hindi:
छात्रवृत्ति आवेदन घोषित अंतिम तिथि से पहले जमा किया जाना चाहिए। देर से प्राप्त आवेदन स्वीकार नहीं किए जा सकते, इसलिए दस्तावेजों की जांच पहले कर लेनी चाहिए।

Gujarati:
શિષ્યવૃત્તિ અરજી જાહેર કરેલી અંતિમ તારીખ પહેલાં જમા કરવી જોઈએ. મોડેથી આવેલી અરજીઓ સ્વીકારવામાં ન આવે તેથી દસ્તાવેજોની તપાસ વહેલી કરવી જોઈએ.
"""
    },

    {
        "id": "d008",
        "category": "scholarship",
        "title": "Scholarship Selection",
        "text": """
English:
Scholarship selection can consider academic merit, financial need, social category, and other eligibility conditions. Each scheme may use a different selection procedure.

Hindi:
छात्रवृत्ति चयन में शैक्षणिक योग्यता, आर्थिक आवश्यकता, सामाजिक श्रेणी और अन्य पात्रता शर्तों पर विचार किया जा सकता है। प्रत्येक योजना की चयन प्रक्रिया अलग हो सकती है।

Gujarati:
શિષ્યવૃત્તિ પસંદગીમાં શૈક્ષણિક લાયકાત, નાણાકીય જરૂરિયાત, સામાજિક વર્ગ અને અન્ય પાત્રતા શરતો ધ્યાનમાં લેવામાં આવી શકે છે. દરેક યોજનાની પસંદગી પ્રક્રિયા અલગ હોઈ શકે છે.
"""
    },

    {
        "id": "d009",
        "category": "scholarship",
        "title": "Scholarship Bank Details",
        "text": """
English:
Applicants may need to provide accurate bank account information to receive scholarship payments. The account should normally belong to the eligible student or approved beneficiary.

Hindi:
छात्रवृत्ति राशि प्राप्त करने के लिए आवेदकों को सही बैंक खाते की जानकारी देनी पड़ सकती है। खाता सामान्यतः पात्र विद्यार्थी या स्वीकृत लाभार्थी का होना चाहिए।

Gujarati:
શિષ્યવૃત્તિની રકમ મેળવવા માટે અરજદારે સાચી બેંક ખાતાની માહિતી આપવી પડી શકે છે. ખાતું સામાન્ય રીતે પાત્ર વિદ્યાર્થી અથવા મંજૂર લાભાર્થીનું હોવું જોઈએ.
"""
    },

    {
        "id": "d010",
        "category": "scholarship",
        "title": "Scholarship Academic Records",
        "text": """
English:
Academic marksheets and enrollment records can be requested during scholarship verification. Students should keep current academic documents available for the application process.

Hindi:
छात्रवृत्ति सत्यापन के दौरान शैक्षणिक अंकपत्र और नामांकन रिकॉर्ड मांगे जा सकते हैं। विद्यार्थियों को आवेदन के लिए वर्तमान शैक्षणिक दस्तावेज उपलब्ध रखने चाहिए।

Gujarati:
શિષ્યવૃત્તિ ચકાસણી દરમિયાન શૈક્ષણિક માર્કશીટ અને પ્રવેશ રેકોર્ડ માંગવામાં આવી શકે છે. વિદ્યાર્થીઓએ અરજી પ્રક્રિયા માટે વર્તમાન શૈક્ષણિક દસ્તાવેજો તૈયાર રાખવા જોઈએ.
"""
    },

    {
        "id": "d011",
        "category": "scholarship",
        "title": "Scholarship Income Certificate",
        "text": """
English:
An income certificate can be used to verify financial eligibility for need-based scholarships. The certificate should be valid and issued by an authorized authority.

Hindi:
आय प्रमाण पत्र का उपयोग आवश्यकता आधारित छात्रवृत्ति के लिए आर्थिक पात्रता सत्यापित करने में किया जा सकता है। प्रमाण पत्र वैध और अधिकृत प्राधिकारी द्वारा जारी होना चाहिए।

Gujarati:
આવક પ્રમાણપત્રનો ઉપયોગ જરૂરિયાત આધારિત શિષ્યવૃત્તિ માટે નાણાકીય પાત્રતા ચકાસવા થઈ શકે છે. પ્રમાણપત્ર માન્ય અને અધિકૃત સત્તા દ્વારા જારી કરેલું હોવું જોઈએ.
"""
    },

    {
        "id": "d012",
        "category": "scholarship",
        "title": "Scholarship Category Requirement",
        "text": """
English:
Certain scholarships are designed for students belonging to specified categories. Applicants may need to submit an appropriate category or community certificate during verification.

Hindi:
कुछ छात्रवृत्तियां विशेष श्रेणी के विद्यार्थियों के लिए बनाई जाती हैं। सत्यापन के दौरान आवेदकों को उपयुक्त श्रेणी या समुदाय प्रमाण पत्र देना पड़ सकता है।

Gujarati:
કેટલીક શિષ્યવૃત્તિ ચોક્કસ વર્ગના વિદ્યાર્થીઓ માટે બનાવવામાં આવે છે. ચકાસણી દરમિયાન અરજદારે યોગ્ય વર્ગ અથવા સમુદાય પ્રમાણપત્ર આપવું પડી શકે છે.
"""
    },

    {
        "id": "d013",
        "category": "scholarship",
        "title": "Scholarship Application Verification",
        "text": """
English:
Scholarship authorities may verify the information submitted by applicants. Incorrect personal details, academic information, or financial documents can delay the application.

Hindi:
छात्रवृत्ति अधिकारी आवेदक द्वारा दी गई जानकारी का सत्यापन कर सकते हैं। गलत व्यक्तिगत जानकारी, शैक्षणिक विवरण या वित्तीय दस्तावेज आवेदन में देरी कर सकते हैं।

Gujarati:
શિષ્યવૃત્તિ સત્તાધિકારીઓ અરજદારે આપેલી માહિતીની ચકાસણી કરી શકે છે. ખોટી વ્યક્તિગત માહિતી, શૈક્ષણિક વિગતો અથવા નાણાકીય દસ્તાવેજો અરજીમાં વિલંબ કરી શકે છે.
"""
    },

    {
        "id": "d014",
        "category": "scholarship",
        "title": "Scholarship Fee Support",
        "text": """
English:
Some scholarship programs help students meet educational expenses such as tuition fees, examination charges, or other approved academic costs.

Hindi:
कुछ छात्रवृत्ति कार्यक्रम विद्यार्थियों के ट्यूशन शुल्क, परीक्षा शुल्क या अन्य स्वीकृत शैक्षणिक खर्चों में सहायता करते हैं।

Gujarati:
કેટલીક શિષ્યવૃત્તિ યોજનાઓ વિદ્યાર્થીઓને ટ્યુશન ફી, પરીક્ષા ફી અથવા અન્ય મંજૂર શૈક્ષણિક ખર્ચમાં સહાય કરે છે.
"""
    },

    {
        "id": "d015",
        "category": "scholarship",
        "title": "Scholarship Application Status",
        "text": """
English:
Applicants can use the scholarship portal to check the status of their application. The status may indicate submission, verification, approval, or a request for additional documents.

Hindi:
आवेदक छात्रवृत्ति पोर्टल पर अपने आवेदन की स्थिति देख सकते हैं। स्थिति में जमा, सत्यापन, स्वीकृति या अतिरिक्त दस्तावेज की मांग दिखाई जा सकती है।

Gujarati:
અરજદારો શિષ્યવૃત્તિ પોર્ટલ પર તેમની અરજીની સ્થિતિ જોઈ શકે છે. સ્થિતિમાં સબમિશન, ચકાસણી, મંજૂરી અથવા વધારાના દસ્તાવેજોની માંગ દર્શાવવામાં આવી શકે છે.
"""
    },

    # --------------------------------------------------------
    # GOVERNMENT SCHEMES: 016-025
    # --------------------------------------------------------

    {
        "id": "d016",
        "category": "government_scheme",
        "title": "Education Financial Support",
        "text": """
English:
Government education schemes can provide financial support to eligible students. Eligibility may depend on income, academic status, category, and scheme conditions.

Hindi:
सरकारी शिक्षा योजनाएं पात्र विद्यार्थियों को वित्तीय सहायता प्रदान कर सकती हैं। पात्रता आय, शैक्षणिक स्थिति, श्रेणी और योजना की शर्तों पर निर्भर हो सकती है।

Gujarati:
સરકારી શિક્ષણ યોજનાઓ પાત્ર વિદ્યાર્થીઓને નાણાકીય સહાય આપી શકે છે. પાત્રતા આવક, શૈક્ષણિક સ્થિતિ, વર્ગ અને યોજનાની શરતો પર આધારિત હોઈ શકે છે.
"""
    },

    {
        "id": "d017",
        "category": "government_scheme",
        "title": "Student Welfare Scheme",
        "text": """
English:
Student welfare schemes may provide assistance for education-related expenses. Students should review eligibility requirements and application instructions before applying.

Hindi:
विद्यार्थी कल्याण योजनाएं शिक्षा से जुड़े खर्चों के लिए सहायता प्रदान कर सकती हैं। आवेदन करने से पहले पात्रता और आवेदन निर्देशों की समीक्षा करनी चाहिए।

Gujarati:
વિદ્યાર્થી કલ્યાણ યોજનાઓ શિક્ષણ સંબંધિત ખર્ચ માટે સહાય આપી શકે છે. અરજી કરતા પહેલાં પાત્રતા અને અરજીની સૂચનાઓ તપાસવી જોઈએ.
"""
    },

    {
        "id": "d018",
        "category": "government_scheme",
        "title": "Government Scheme Income Limit",
        "text": """
English:
Several government student schemes use annual family income as an eligibility criterion. Applicants may need to provide an income certificate to demonstrate that they satisfy the prescribed limit.

Hindi:
कई सरकारी विद्यार्थी योजनाओं में वार्षिक पारिवारिक आय पात्रता का मानदंड होती है। निर्धारित सीमा पूरी करने के लिए आय प्रमाण पत्र देना पड़ सकता है।

Gujarati:
ઘણી સરકારી વિદ્યાર્થી યોજનાઓમાં વાર્ષિક પરિવારની આવક પાત્રતાનો માપદંડ હોય છે. નક્કી કરેલી મર્યાદા દર્શાવવા માટે આવક પ્રમાણપત્ર આપવું પડી શકે છે.
"""
    },

    {
        "id": "d019",
        "category": "government_scheme",
        "title": "Government Scheme Registration",
        "text": """
English:
Students may need to register through an official government portal to access education schemes. Registration usually involves personal and academic information.

Hindi:
शिक्षा योजनाओं का लाभ लेने के लिए विद्यार्थियों को आधिकारिक सरकारी पोर्टल पर पंजीकरण करना पड़ सकता है। पंजीकरण में व्यक्तिगत और शैक्षणिक जानकारी मांगी जाती है।

Gujarati:
શિક્ષણ યોજનાઓનો લાભ લેવા માટે વિદ્યાર્થીઓએ સત્તાવાર સરકારી પોર્ટલ પર નોંધણી કરવી પડી શકે છે. નોંધણીમાં વ્યક્તિગત અને શૈક્ષણિક માહિતી માંગવામાં આવે છે.
"""
    },

    {
        "id": "d020",
        "category": "government_scheme",
        "title": "Government Scheme Documents",
        "text": """
English:
Government education assistance applications may require identity proof, enrollment records, income certificates, and bank information.

Hindi:
सरकारी शिक्षा सहायता के आवेदन में पहचान प्रमाण, नामांकन रिकॉर्ड, आय प्रमाण पत्र और बैंक जानकारी की आवश्यकता हो सकती है।

Gujarati:
સરકારી શિક્ષણ સહાયની અરજીમાં ઓળખનો પુરાવો, પ્રવેશ રેકોર્ડ, આવક પ્રમાણપત્ર અને બેંક માહિતી જરૂરી હોઈ શકે છે.
"""
    },

    {
        "id": "d021",
        "category": "government_scheme",
        "title": "Government Scheme Renewal",
        "text": """
English:
Some student welfare schemes require annual renewal. Students may need to confirm continued eligibility and submit updated documents.

Hindi:
कुछ विद्यार्थी कल्याण योजनाओं में हर वर्ष नवीनीकरण आवश्यक होता है। विद्यार्थियों को निरंतर पात्रता की पुष्टि और अद्यतन दस्तावेज जमा करने पड़ सकते हैं।

Gujarati:
કેટલીક વિદ્યાર્થી કલ્યાણ યોજનાઓમાં દર વર્ષે નવીકરણ જરૂરી હોય છે. વિદ્યાર્થીઓએ સતત પાત્રતાની પુષ્ટિ કરી અને અપડેટ દસ્તાવેજો જમા કરવા પડી શકે છે.
"""
    },

    {
        "id": "d022",
        "category": "government_scheme",
        "title": "Government Education Benefit",
        "text": """
English:
Education schemes may support tuition fees, study materials, accommodation, or other approved educational expenses depending on the specific program.

Hindi:
शिक्षा योजनाएं कार्यक्रम के अनुसार ट्यूशन शुल्क, अध्ययन सामग्री, आवास या अन्य स्वीकृत शैक्षणिक खर्चों में सहायता कर सकती हैं।

Gujarati:
શિક્ષણ યોજનાઓ ચોક્કસ કાર્યક્રમ અનુસાર ટ્યુશન ફી, અભ્યાસ સામગ્રી, રહેઠાણ અથવા અન્ય મંજૂર શૈક્ષણિક ખર્ચમાં સહાય કરી શકે છે.
"""
    },

    {
        "id": "d023",
        "category": "government_scheme",
        "title": "Government Scheme Category",
        "text": """
English:
Some government education programs target students from particular social or economic categories. Supporting certificates may be required during application verification.

Hindi:
कुछ सरकारी शिक्षा कार्यक्रम विशेष सामाजिक या आर्थिक श्रेणी के विद्यार्थियों के लिए होते हैं। आवेदन सत्यापन के दौरान संबंधित प्रमाण पत्र आवश्यक हो सकते हैं।

Gujarati:
કેટલાક સરકારી શિક્ષણ કાર્યક્રમો ચોક્કસ સામાજિક અથવા આર્થિક વર્ગના વિદ્યાર્થીઓ માટે હોય છે. અરજીની ચકાસણી દરમિયાન સંબંધિત પ્રમાણપત્રો જરૂરી હોઈ શકે છે.
"""
    },

    {
        "id": "d024",
        "category": "government_scheme",
        "title": "Government Scheme Deadline",
        "text": """
English:
Students should submit government education scheme applications before the announced deadline. Portal submission after the closing date may not be accepted.

Hindi:
विद्यार्थियों को सरकारी शिक्षा योजना के आवेदन घोषित अंतिम तिथि से पहले जमा करने चाहिए। अंतिम तिथि के बाद पोर्टल पर आवेदन स्वीकार नहीं हो सकता है।

Gujarati:
વિદ્યાર્થીઓએ સરકારી શિક્ષણ યોજનાની અરજી જાહેર કરેલી અંતિમ તારીખ પહેલાં જમા કરવી જોઈએ. અંતિમ તારીખ પછી પોર્ટલ પર અરજી સ્વીકારવામાં ન આવે.
"""
    },

    {
        "id": "d025",
        "category": "government_scheme",
        "title": "Government Scheme Application Tracking",
        "text": """
English:
Applicants can track the progress of a government education assistance application through the official portal. Status information may show verification or approval progress.

Hindi:
आवेदक आधिकारिक पोर्टल के माध्यम से सरकारी शिक्षा सहायता आवेदन की प्रगति देख सकते हैं। स्थिति में सत्यापन या स्वीकृति की जानकारी दिखाई जा सकती है।

Gujarati:
અરજદારો સત્તાવાર પોર્ટલ દ્વારા સરકારી શિક્ષણ સહાયની અરજીની પ્રગતિ જોઈ શકે છે. સ્થિતિમાં ચકાસણી અથવા મંજૂરીની માહિતી દેખાઈ શકે છે.
"""
    },

    # --------------------------------------------------------
    # HOSTEL: 026-032
    # --------------------------------------------------------

    {
        "id": "d026",
        "category": "hostel",
        "title": "Hostel Application",
        "text": """
English:
Students seeking hostel accommodation should complete the hostel application form and submit required admission and identification documents before the deadline.

Hindi:
छात्रावास आवास चाहने वाले विद्यार्थियों को छात्रावास आवेदन पत्र भरना चाहिए और अंतिम तिथि से पहले आवश्यक प्रवेश तथा पहचान दस्तावेज जमा करने चाहिए।

Gujarati:
હોસ્ટેલ રહેઠાણ મેળવવા ઇચ્છતા વિદ્યાર્થીઓએ હોસ્ટેલ અરજી ફોર્મ ભરવું અને અંતિમ તારીખ પહેલાં જરૂરી પ્રવેશ તથા ઓળખ દસ્તાવેજો જમા કરવા જોઈએ.
"""
    },

    {
        "id": "d027",
        "category": "hostel",
        "title": "Hostel Eligibility",
        "text": """
English:
Hostel accommodation is generally available to eligible enrolled students. Institutions may give preference based on distance from home, academic status, or other hostel rules.

Hindi:
छात्रावास की सुविधा सामान्यतः पात्र नामांकित विद्यार्थियों के लिए उपलब्ध होती है। संस्थान घर से दूरी, शैक्षणिक स्थिति या अन्य नियमों के आधार पर प्राथमिकता दे सकते हैं।

Gujarati:
હોસ્ટેલની સુવિધા સામાન્ય રીતે પાત્ર નોંધાયેલા વિદ્યાર્થીઓ માટે ઉપલબ્ધ હોય છે. સંસ્થાઓ ઘરથી અંતર, શૈક્ષણિક સ્થિતિ અથવા અન્ય નિયમોના આધારે પ્રાથમિકતા આપી શકે છે.
"""
    },

    {
        "id": "d028",
        "category": "hostel",
        "title": "Hostel Documents",
        "text": """
English:
Hostel applications may require admission proof, student identification, photographs, and other documents specified by the institution.

Hindi:
छात्रावास आवेदन में प्रवेश प्रमाण, विद्यार्थी पहचान पत्र, फोटो और संस्थान द्वारा बताए गए अन्य दस्तावेज मांगे जा सकते हैं।

Gujarati:
હોસ્ટેલ અરજીમાં પ્રવેશનો પુરાવો, વિદ્યાર્થી ઓળખપત્ર, ફોટોગ્રાફ અને સંસ્થા દ્વારા જણાવેલા અન્ય દસ્તાવેજો જરૂરી હોઈ શકે છે.
"""
    },

    {
        "id": "d029",
        "category": "hostel",
        "title": "Hostel Fee",
        "text": """
English:
Students allotted hostel accommodation must pay the applicable hostel fee within the specified period. The fee may cover room, maintenance, and approved hostel services.

Hindi:
छात्रावास आवंटित होने पर विद्यार्थियों को निर्धारित अवधि में लागू छात्रावास शुल्क का भुगतान करना होता है। शुल्क में कमरा, रखरखाव और अन्य सेवाएं शामिल हो सकती हैं।

Gujarati:
હોસ્ટેલ ફાળવવામાં આવ્યા પછી વિદ્યાર્થીઓએ નિર્ધારિત સમયગાળામાં લાગુ હોસ્ટેલ ફી ચૂકવવી પડે છે. ફીમાં રૂમ, જાળવણી અને અન્ય સેવાઓનો સમાવેશ થઈ શકે છે.
"""
    },

    {
        "id": "d030",
        "category": "hostel",
        "title": "Hostel Allocation",
        "text": """
English:
Hostel rooms are allocated according to institutional rules and available capacity. Applicants may receive an allotment notice after the selection process.

Hindi:
छात्रावास के कमरे संस्थान के नियमों और उपलब्ध क्षमता के अनुसार आवंटित किए जाते हैं। चयन प्रक्रिया के बाद आवेदकों को आवंटन सूचना मिल सकती है।

Gujarati:
હોસ્ટેલના રૂમ સંસ્થાના નિયમો અને ઉપલબ્ધ ક્ષમતા અનુસાર ફાળવવામાં આવે છે. પસંદગી પ્રક્રિયા પછી અરજદારોને ફાળવણીની સૂચના મળી શકે છે.
"""
    },

    {
        "id": "d031",
        "category": "hostel",
        "title": "Hostel Renewal",
        "text": """
English:
Students continuing in hostel accommodation may need to complete a renewal process for the next academic term. Updated information and fee payment may be required.

Hindi:
छात्रावास में रहने वाले विद्यार्थियों को अगले शैक्षणिक सत्र के लिए नवीनीकरण प्रक्रिया पूरी करनी पड़ सकती है। अद्यतन जानकारी और शुल्क भुगतान आवश्यक हो सकता है।

Gujarati:
હોસ્ટેલમાં રહેતા વિદ્યાર્થીઓએ આગામી શૈક્ષણિક સત્ર માટે નવીકરણ પ્રક્રિયા પૂર્ણ કરવી પડી શકે છે. અપડેટ માહિતી અને ફી ચુકવણી જરૂરી હોઈ શકે છે.
"""
    },

    {
        "id": "d032",
        "category": "hostel",
        "title": "Hostel Rules",
        "text": """
English:
Hostel residents must follow institutional accommodation rules covering attendance, visitors, room use, cleanliness, and conduct.

Hindi:
छात्रावास में रहने वाले विद्यार्थियों को उपस्थिति, आगंतुक, कमरे के उपयोग, स्वच्छता और आचरण से संबंधित संस्थागत नियमों का पालन करना होता है।

Gujarati:
હોસ્ટેલમાં રહેતા વિદ્યાર્થીઓએ હાજરી, મુલાકાતીઓ, રૂમનો ઉપયોગ, સ્વચ્છતા અને વર્તન સંબંધિત સંસ્થાના નિયમોનું પાલન કરવું પડે છે.
"""
    },

    # --------------------------------------------------------
    # EXAMINATION: 033-039
    # --------------------------------------------------------

    {
        "id": "d033",
        "category": "examination",
        "title": "Examination Registration",
        "text": """
English:
University examination registration normally requires student enrollment information and payment of the applicable examination fee before the deadline.

Hindi:
विश्वविद्यालय परीक्षा पंजीकरण के लिए सामान्यतः विद्यार्थी का नामांकन विवरण और लागू परीक्षा शुल्क का भुगतान अंतिम तिथि से पहले आवश्यक होता है।

Gujarati:
યુનિવર્સિટી પરીક્ષા નોંધણી માટે સામાન્ય રીતે વિદ્યાર્થીની નોંધણી માહિતી અને લાગુ પરીક્ષા ફીની ચુકવણી અંતિમ તારીખ પહેલાં જરૂરી હોય છે.
"""
    },

    {
        "id": "d034",
        "category": "examination",
        "title": "Examination Fee",
        "text": """
English:
Students must pay the prescribed examination fee during examination registration. The payment receipt may be required as evidence of successful registration.

Hindi:
परीक्षा पंजीकरण के दौरान विद्यार्थियों को निर्धारित परीक्षा शुल्क जमा करना होता है। सफल पंजीकरण के प्रमाण के रूप में भुगतान रसीद आवश्यक हो सकती है।

Gujarati:
પરીક્ષા નોંધણી દરમિયાન વિદ્યાર્થીઓએ નિર્ધારિત પરીક્ષા ફી ચૂકવવી પડે છે. સફળ નોંધણીના પુરાવા તરીકે ચુકવણીની રસીદ જરૂરી હોઈ શકે છે.
"""
    },

    {
        "id": "d035",
        "category": "examination",
        "title": "Examination Form",
        "text": """
English:
Students should verify course selections and personal information before submitting the examination form. Errors should be reported according to institutional procedures.

Hindi:
परीक्षा फॉर्म जमा करने से पहले विद्यार्थियों को विषय चयन और व्यक्तिगत जानकारी जांचनी चाहिए। त्रुटियों की सूचना संस्थान की प्रक्रिया के अनुसार देनी चाहिए।

Gujarati:
પરીક્ષા ફોર્મ જમા કરતા પહેલાં વિદ્યાર્થીઓએ વિષય પસંદગી અને વ્યક્તિગત માહિતી તપાસવી જોઈએ. ભૂલોની જાણ સંસ્થાની પ્રક્રિયા મુજબ કરવી જોઈએ.
"""
    },

    {
        "id": "d036",
        "category": "examination",
        "title": "Examination Registration Deadline",
        "text": """
English:
Examination registration must be completed before the published deadline. Students should avoid waiting until the final day because technical or payment problems may occur.

Hindi:
परीक्षा पंजीकरण प्रकाशित अंतिम तिथि से पहले पूरा करना चाहिए। विद्यार्थियों को अंतिम दिन तक प्रतीक्षा नहीं करनी चाहिए क्योंकि तकनीकी या भुगतान संबंधी समस्या हो सकती है।

Gujarati:
પરીક્ષા નોંધણી જાહેર કરેલી અંતિમ તારીખ પહેલાં પૂર્ણ કરવી જોઈએ. વિદ્યાર્થીઓએ છેલ્લી તારીખ સુધી રાહ ન જોવી જોઈએ કારણ કે તકનીકી અથવા ચુકવણીની સમસ્યા થઈ શકે છે.
"""
    },

    {
        "id": "d037",
        "category": "examination",
        "title": "Examination Admit Card",
        "text": """
English:
After successful examination registration, students may receive an admit card containing examination details. The admit card should be checked for course, date, and examination center information.

Hindi:
सफल परीक्षा पंजीकरण के बाद विद्यार्थियों को परीक्षा विवरण वाला प्रवेश पत्र मिल सकता है। प्रवेश पत्र में विषय, तिथि और परीक्षा केंद्र की जानकारी जांचनी चाहिए।

Gujarati:
સફળ પરીક્ષા નોંધણી પછી વિદ્યાર્થીઓને પરીક્ષાની વિગતો ધરાવતું પ્રવેશપત્ર મળી શકે છે. પ્રવેશપત્રમાં વિષય, તારીખ અને પરીક્ષા કેન્દ્રની માહિતી તપાસવી જોઈએ.
"""
    },

    {
        "id": "d038",
        "category": "examination",
        "title": "Examination Course Registration",
        "text": """
English:
Students should ensure that all eligible courses are correctly included in the examination registration form. Missing a course can affect examination participation.

Hindi:
विद्यार्थियों को सुनिश्चित करना चाहिए कि सभी पात्र विषय परीक्षा पंजीकरण फॉर्म में सही ढंग से शामिल हों। किसी विषय के छूटने से परीक्षा में भाग लेने पर प्रभाव पड़ सकता है।

Gujarati:
વિદ્યાર્થીઓએ ખાતરી કરવી જોઈએ કે તમામ પાત્ર વિષયો પરીક્ષા નોંધણી ફોર્મમાં યોગ્ય રીતે સામેલ છે. કોઈ વિષય છૂટી જવાથી પરીક્ષામાં ભાગ લેવામાં અસર થઈ શકે છે.
"""
    },

    {
        "id": "d039",
        "category": "examination",
        "title": "Examination Registration Correction",
        "text": """
English:
If incorrect information is submitted during examination registration, students should contact the appropriate academic office or follow the institution's correction procedure.

Hindi:
यदि परीक्षा पंजीकरण के दौरान गलत जानकारी जमा हो जाए, तो विद्यार्थियों को संबंधित शैक्षणिक कार्यालय से संपर्क करना चाहिए या संस्थान की सुधार प्रक्रिया का पालन करना चाहिए।

Gujarati:
પરીક્ષા નોંધણી દરમિયાન ખોટી માહિતી જમા થાય તો વિદ્યાર્થીઓએ સંબંધિત શૈક્ષણિક કચેરીનો સંપર્ક કરવો અથવા સંસ્થાની સુધારણા પ્રક્રિયાનું પાલન કરવું જોઈએ.
"""
    },

    # --------------------------------------------------------
    # FINANCIAL ASSISTANCE: 040-045
    # --------------------------------------------------------

    {
        "id": "d040",
        "category": "financial_assistance",
        "title": "Student Financial Assistance",
        "text": """
English:
Educational institutions may provide financial assistance through scholarships, fee concessions, emergency aid, or other student support programs.

Hindi:
शैक्षणिक संस्थान छात्रवृत्ति, शुल्क में छूट, आपातकालीन सहायता या अन्य विद्यार्थी सहायता कार्यक्रमों के माध्यम से वित्तीय सहायता दे सकते हैं।

Gujarati:
શૈક્ષણિક સંસ્થાઓ શિષ્યવૃત્તિ, ફીમાં છૂટ, કટોકટી સહાય અથવા અન્ય વિદ્યાર્થી સહાય કાર્યક્રમો દ્વારા નાણાકીય સહાય આપી શકે છે.
"""
    },

    {
        "id": "d041",
        "category": "financial_assistance",
        "title": "Fee Concession",
        "text": """
English:
Eligible students may receive fee concessions based on financial need, academic merit, or institutional policy. Supporting documents may be requested.

Hindi:
पात्र विद्यार्थियों को आर्थिक आवश्यकता, शैक्षणिक योग्यता या संस्थागत नीति के आधार पर शुल्क में छूट मिल सकती है। सहायक दस्तावेज मांगे जा सकते हैं।

Gujarati:
પાત્ર વિદ્યાર્થીઓને નાણાકીય જરૂરિયાત, શૈક્ષણિક લાયકાત અથવા સંસ્થાની નીતિના આધારે ફીમાં છૂટ મળી શકે છે. સહાયક દસ્તાવેજો માંગવામાં આવી શકે છે.
"""
    },

    {
        "id": "d042",
        "category": "financial_assistance",
        "title": "Emergency Student Aid",
        "text": """
English:
Emergency financial assistance may help students facing unexpected educational expenses. Applicants may need to explain the circumstances and provide supporting evidence.

Hindi:
आपातकालीन वित्तीय सहायता अचानक आने वाले शैक्षणिक खर्चों का सामना कर रहे विद्यार्थियों की मदद कर सकती है। आवेदकों को परिस्थिति समझाकर प्रमाण देना पड़ सकता है।

Gujarati:
કટોકટી નાણાકીય સહાય અચાનક આવેલા શૈક્ષણિક ખર્ચનો સામનો કરતા વિદ્યાર્થીઓને મદદ કરી શકે છે. અરજદારે પરિસ્થિતિ સમજાવી અને પુરાવા આપવા પડી શકે છે.
"""
    },

    {
        "id": "d043",
        "category": "financial_assistance",
        "title": "Financial Need Assessment",
        "text": """
English:
Financial assistance programs may assess family income, number of dependents, existing educational expenses, and other indicators of financial need.

Hindi:
वित्तीय सहायता कार्यक्रम पारिवारिक आय, आश्रितों की संख्या, मौजूदा शैक्षणिक खर्च और आर्थिक आवश्यकता के अन्य संकेतकों का मूल्यांकन कर सकते हैं।

Gujarati:
નાણાકીય સહાય કાર્યક્રમો પરિવારની આવક, આશ્રિતોની સંખ્યા, વર્તમાન શૈક્ષણિક ખર્ચ અને નાણાકીય જરૂરિયાતના અન્ય સૂચકોનું મૂલ્યાંકન કરી શકે છે.
"""
    },

    {
        "id": "d044",
        "category": "financial_assistance",
        "title": "Financial Aid Documents",
        "text": """
English:
Applications for financial aid may require income proof, fee records, bank information, and identification documents.

Hindi:
वित्तीय सहायता के आवेदन में आय प्रमाण, शुल्क रिकॉर्ड, बैंक जानकारी और पहचान दस्तावेज आवश्यक हो सकते हैं।

Gujarati:
નાણાકીય સહાયની અરજી માટે આવકનો પુરાવો, ફી રેકોર્ડ, બેંક માહિતી અને ઓળખ દસ્તાવેજો જરૂરી હોઈ શકે છે.
"""
    },

    {
        "id": "d045",
        "category": "financial_assistance",
        "title": "Financial Aid Application",
        "text": """
English:
Students requesting financial aid should complete the prescribed application and provide accurate information about their financial circumstances.

Hindi:
वित्तीय सहायता मांगने वाले विद्यार्थियों को निर्धारित आवेदन पूरा करना चाहिए और अपनी आर्थिक स्थिति के बारे में सही जानकारी देनी चाहिए।

Gujarati:
નાણાકીય સહાય માંગતા વિદ્યાર્થીઓએ નિર્ધારિત અરજી પૂર્ણ કરવી અને તેમની નાણાકીય પરિસ્થિતિ વિશે સાચી માહિતી આપવી જોઈએ.
"""
    },

    # --------------------------------------------------------
    # ADMISSIONS: 046-050
    # --------------------------------------------------------

    {
        "id": "d046",
        "category": "admission",
        "title": "University Admission Documents",
        "text": """
English:
University admission may require academic certificates, identity proof, photographs, and other documents specified by the institution.

Hindi:
विश्वविद्यालय प्रवेश के लिए शैक्षणिक प्रमाण पत्र, पहचान प्रमाण, फोटो और संस्थान द्वारा बताए गए अन्य दस्तावेज आवश्यक हो सकते हैं।

Gujarati:
યુનિવર્સિટી પ્રવેશ માટે શૈક્ષણિક પ્રમાણપત્રો, ઓળખનો પુરાવો, ફોટોગ્રાફ અને સંસ્થા દ્વારા જણાવેલા અન્ય દસ્તાવેજો જરૂરી હોઈ શકે છે.
"""
    },

    {
        "id": "d047",
        "category": "admission",
        "title": "Admission Eligibility",
        "text": """
English:
Admission eligibility depends on the academic qualification, entrance requirements, program rules, and other conditions specified by the institution.

Hindi:
प्रवेश पात्रता शैक्षणिक योग्यता, प्रवेश आवश्यकताओं, कार्यक्रम के नियमों और संस्थान द्वारा निर्धारित अन्य शर्तों पर निर्भर करती है।

Gujarati:
પ્રવેશ પાત્રતા શૈક્ષણિક લાયકાત, પ્રવેશની આવશ્યકતાઓ, કાર્યક્રમના નિયમો અને સંસ્થા દ્વારા નક્કી કરેલી અન્ય શરતો પર આધારિત છે.
"""
    },

    {
        "id": "d048",
        "category": "admission",
        "title": "Admission Fee",
        "text": """
English:
Selected students must complete admission fee payment within the specified period to confirm their seat. Payment instructions are normally provided by the institution.

Hindi:
चयनित विद्यार्थियों को अपनी सीट सुनिश्चित करने के लिए निर्धारित समय में प्रवेश शुल्क जमा करना होता है। भुगतान के निर्देश संस्थान द्वारा दिए जाते हैं।

Gujarati:
પસંદ થયેલા વિદ્યાર્થીઓએ પોતાની સીટની પુષ્ટિ કરવા માટે નિર્ધારિત સમયગાળામાં પ્રવેશ ફી ચૂકવવી પડે છે. ચુકવણીની સૂચનાઓ સંસ્થા દ્વારા આપવામાં આવે છે.
"""
    },

    {
        "id": "d049",
        "category": "admission",
        "title": "Admission Verification",
        "text": """
English:
During admission verification, institutions may compare submitted documents with original certificates. Students should bring valid original documents when requested.

Hindi:
प्रवेश सत्यापन के दौरान संस्थान जमा किए गए दस्तावेजों की मूल प्रमाणपत्रों से तुलना कर सकते हैं। मांग किए जाने पर विद्यार्थियों को वैध मूल दस्तावेज लाने चाहिए।

Gujarati:
પ્રવેશ ચકાસણી દરમિયાન સંસ્થાઓ જમા કરેલા દસ્તાવેજોની મૂળ પ્રમાણપત્રો સાથે સરખામણી કરી શકે છે. માંગ કરવામાં આવે ત્યારે વિદ્યાર્થીઓએ માન્ય મૂળ દસ્તાવેજો લાવવા જોઈએ.
"""
    },

    {
        "id": "d050",
        "category": "admission",
        "title": "Admission Deadline",
        "text": """
English:
Students offered admission should complete the required admission formalities before the announced deadline. Failure to complete the process may result in loss of the offered seat.

Hindi:
प्रवेश की पेशकश पाने वाले विद्यार्थियों को घोषित अंतिम तिथि से पहले आवश्यक प्रवेश औपचारिकताएं पूरी करनी चाहिए। प्रक्रिया पूरी न करने पर सीट खो सकती है।

Gujarati:
પ્રવેશની ઓફર મેળવનારા વિદ્યાર્થીઓએ જાહેર કરેલી અંતિમ તારીખ પહેલાં જરૂરી પ્રવેશ પ્રક્રિયા પૂર્ણ કરવી જોઈએ. પ્રક્રિયા પૂર્ણ ન કરવાથી મળેલી સીટ ગુમાવી શકાય છે.
"""
    }
]


# ============================================================
# EVALUATION QUERIES
# 30 queries
# ============================================================

queries = [

    # Scholarship - English
    {
        "query_id": "q001",
        "language": "en",
        "query": "What are the eligibility requirements for a student scholarship?",
        "relevant_docs": ["d001", "d004", "d008"]
    },
    {
        "query_id": "q002",
        "language": "en",
        "query": "What documents are required for a scholarship application?",
        "relevant_docs": ["d002", "d005", "d010"]
    },
    {
        "query_id": "q003",
        "language": "en",
        "query": "How are merit scholarships awarded?",
        "relevant_docs": ["d003"]
    },
    {
        "query_id": "q004",
        "language": "en",
        "query": "How can students renew a scholarship?",
        "relevant_docs": ["d006"]
    },
    {
        "query_id": "q005",
        "language": "en",
        "query": "Why is an income certificate needed for scholarships?",
        "relevant_docs": ["d004", "d011"]
    },

    # Scholarship - Hindi
    {
        "query_id": "q006",
        "language": "hi",
        "query": "छात्रवृत्ति के लिए कौन से दस्तावेज आवश्यक हैं?",
        "relevant_docs": ["d002", "d010"]
    },
    {
        "query_id": "q007",
        "language": "hi",
        "query": "मेधावी छात्रवृत्ति किस आधार पर दी जाती है?",
        "relevant_docs": ["d003"]
    },
    {
        "query_id": "q008",
        "language": "hi",
        "query": "छात्रवृत्ति की अंतिम तिथि क्यों महत्वपूर्ण है?",
        "relevant_docs": ["d007"]
    },
    {
        "query_id": "q009",
        "language": "hi",
        "query": "छात्रवृत्ति आवेदन की स्थिति कैसे देख सकते हैं?",
        "relevant_docs": ["d015"]
    },
    {
        "query_id": "q010",
        "language": "hi",
        "query": "आय प्रमाण पत्र छात्रवृत्ति में क्यों आवश्यक है?",
        "relevant_docs": ["d004", "d011"]
    },

    # Scholarship - Gujarati
    {
        "query_id": "q011",
        "language": "gu",
        "query": "શિષ્યવૃત્તિ માટે કયા દસ્તાવેજો જરૂરી છે?",
        "relevant_docs": ["d002", "d005"]
    },
    {
        "query_id": "q012",
        "language": "gu",
        "query": "મેરિટ શિષ્યવૃત્તિ કયા આધારે આપવામાં આવે છે?",
        "relevant_docs": ["d003"]
    },
    {
        "query_id": "q013",
        "language": "gu",
        "query": "આર્થિક રીતે નબળા વિદ્યાર્થીઓ માટે શિષ્યવૃત્તિ કેવી રીતે મળે છે?",
        "relevant_docs": ["d004", "d016"]
    },
    {
        "query_id": "q014",
        "language": "gu",
        "query": "શિષ્યવૃત્તિ અરજીની સ્થિતિ કેવી રીતે તપાસી શકાય?",
        "relevant_docs": ["d015"]
    },
    {
        "query_id": "q015",
        "language": "gu",
        "query": "શિષ્યવૃત્તિ માટે આવક પ્રમાણપત્ર શા માટે જરૂરી છે?",
        "relevant_docs": ["d011"]
    },

    # Government schemes
    {
        "query_id": "q016",
        "language": "en",
        "query": "How can students register for a government education scheme?",
        "relevant_docs": ["d019"]
    },
    {
        "query_id": "q017",
        "language": "hi",
        "query": "सरकारी शिक्षा योजना के लिए आय सीमा कैसे तय होती है?",
        "relevant_docs": ["d018"]
    },
    {
        "query_id": "q018",
        "language": "gu",
        "query": "સરકારી શિક્ષણ યોજનામાં કયા દસ્તાવેજો જરૂરી છે?",
        "relevant_docs": ["d020"]
    },
    {
        "query_id": "q019",
        "language": "en",
        "query": "What expenses can government education schemes support?",
        "relevant_docs": ["d022"]
    },
    {
        "query_id": "q020",
        "language": "hi",
        "query": "सरकारी विद्यार्थी योजना का नवीनीकरण कैसे किया जाता है?",
        "relevant_docs": ["d021"]
    },

    # Hostel
    {
        "query_id": "q021",
        "language": "gu",
        "query": "હોસ્ટેલ માટે વિદ્યાર્થીઓ કેવી રીતે અરજી કરી શકે?",
        "relevant_docs": ["d026"]
    },
    {
        "query_id": "q022",
        "language": "hi",
        "query": "छात्रावास आवेदन के लिए कौन से दस्तावेज चाहिए?",
        "relevant_docs": ["d028"]
    },
    {
        "query_id": "q023",
        "language": "en",
        "query": "How is hostel accommodation allocated?",
        "relevant_docs": ["d030"]
    },

    # Examination
    {
        "query_id": "q024",
        "language": "en",
        "query": "What is required for university examination registration?",
        "relevant_docs": ["d033", "d034"]
    },
    {
        "query_id": "q025",
        "language": "hi",
        "query": "परीक्षा पंजीकरण की अंतिम तिथि कब महत्वपूर्ण होती है?",
        "relevant_docs": ["d036"]
    },
    {
        "query_id": "q026",
        "language": "gu",
        "query": "પરીક્ષા ફોર્મમાં વિષયની માહિતી કેમ તપાસવી જોઈએ?",
        "relevant_docs": ["d035", "d038"]
    },

    # Financial assistance
    {
        "query_id": "q027",
        "language": "en",
        "query": "What types of financial assistance can students receive?",
        "relevant_docs": ["d040", "d022"]
    },
    {
        "query_id": "q028",
        "language": "hi",
        "query": "वित्तीय सहायता के लिए कौन से दस्तावेज आवश्यक हो सकते हैं?",
        "relevant_docs": ["d044"]
    },

    # Admissions
    {
        "query_id": "q029",
        "language": "gu",
        "query": "યુનિવર્સિટી પ્રવેશ માટે કયા દસ્તાવેજો જરૂરી છે?",
        "relevant_docs": ["d046"]
    },
    {
        "query_id": "q030",
        "language": "en",
        "query": "What determines university admission eligibility?",
        "relevant_docs": ["d047"]
    }
]


# ============================================================
# WRITE DATASET
# ============================================================

def main():

    DOCUMENT_DIR.mkdir(parents=True, exist_ok=True)
    QUERY_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Write documents
    for document in documents:

        file_path = DOCUMENT_DIR / f"{document['id']}.txt"

        content = (
            f"Title: {document['title']}\n"
            f"Category: {document['category']}\n"
            f"\n"
            f"{document['text'].strip()}\n"
        )

        file_path.write_text(
            content,
            encoding="utf-8"
        )

    # Write queries
    QUERY_FILE.write_text(
        json.dumps(
            queries,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print("=" * 65)
    print("IndicSeek - Development Dataset Created")
    print("=" * 65)

    print(f"\nDocuments created: {len(documents)}")
    print(f"Queries created:   {len(queries)}")

    print("\nDocument categories:")

    categories = {}

    for document in documents:
        category = document["category"]
        categories[category] = categories.get(category, 0) + 1

    for category, count in categories.items():
        print(f"  {category:20s}: {count}")

    print("\nLanguages:")
    print("  English")
    print("  Hindi")
    print("  Gujarati")

    print("\nDocument directory:")
    print(DOCUMENT_DIR)

    print("\nQuery file:")
    print(QUERY_FILE)

    print("\nDataset type:")
    print("Synthetic controlled development corpus")

    print("\nReady for retrieval evaluation.")


if __name__ == "__main__":
    main()