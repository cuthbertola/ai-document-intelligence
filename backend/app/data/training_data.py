"""Comprehensive training data for document classification"""

TRAINING_DOCUMENTS = {
    'resume': [
        # Original resumes
        "John Doe Software Engineer Email: john@email.com PROFESSIONAL SUMMARY Results-driven software engineer with 5 years experience WORK EXPERIENCE Senior Engineer at Tech Corp 2020-Present Developed microservices Led team of 4 engineers EDUCATION Bachelor of Science in Computer Science University 2018 GPA 3.8 SKILLS Python JavaScript React Docker AWS SQL",
        "Sarah Johnson Marketing Manager PROFESSIONAL PROFILE Creative marketing professional EXPERIENCE Marketing Manager Brand Solutions 2019-Present Managed 2M budget Increased lead generation 150 percent MBA in Marketing 2017 CERTIFICATIONS Google Analytics Certified",
        "Michael Chen Data Scientist SUMMARY Data scientist specializing in machine learning PROFESSIONAL EXPERIENCE Senior Data Scientist AI Solutions 2021-Present Built ML models 95 percent accuracy MS in Data Science 2019 TECHNICAL SKILLS Machine Learning Deep Learning NLP",
        "Emily Rodriguez Project Manager Professional Experience Project Manager Innovation Labs 2019-Present Successfully delivered 15 projects Managed teams of 20 members Certifications PMP Scrum Master Education MBA Project Management",
        "David Kim Financial Analyst Work History Financial Analyst Goldman Sachs 2020-Present Financial modeling forecasting Bachelor Business Administration Finance 2019 Technical Skills Excel SQL Python Tableau",
        "Lisa Chang UX Designer Creative designer passionate about user-centered design Senior UX Designer Airbnb 2021-Present Led mobile app redesign improving engagement 45 percent BFA Graphic Design Tools Figma Sketch Adobe",
        
        # Additional resume variations
        "CURRICULUM VITAE James Wilson PhD Candidate Research Experience Graduate Research Assistant MIT 2020-Present Published 5 peer-reviewed papers Education PhD Computer Science MIT 2019-2025 MS Computer Science Stanford 2019 Skills Research Python TensorFlow Publications",
        "Resume Amanda Martinez Registered Nurse RN Professional Summary Compassionate healthcare professional 8 years experience Clinical Experience Staff Nurse General Hospital 2016-Present Patient care Medication administration Education BSN Nursing University 2015 Certifications ACLS BLS",
        "CV Thomas Anderson Mechanical Engineer PE Work Experience Senior Engineer Boeing 2018-Present Aircraft systems design CAD modeling Education Bachelor Mechanical Engineering Purdue 2017 Professional Engineer License Technical Skills SolidWorks MATLAB FEA",
        "RESUME Maria Garcia HR Manager Professional Experience Human Resources Manager Tech Startup 2019-Present Recruitment Employee relations Benefits administration Education MBA Human Resources Management Skills Talent Acquisition Performance Management HRIS",
        "Career Profile Robert Lee Sales Director Professional Background Regional Sales Director Fortune 500 Company 2017-Present Team leadership Revenue growth CRM management Education BBA Marketing State University Skills Salesforce Negotiation Territory Management",
        "Professional Resume Jessica Taylor Graphic Designer Creative Professional Portfolio: jessicataylor.design Experience Senior Designer Creative Agency 2018-Present Brand identity Web design Print media Education BFA Graphic Design Art Institute Tools Adobe Creative Suite",
    ],
    
    'invoice': [
        # Original invoices
        "INVOICE INV-2024-001 Bill To ABC Corporation Date November 16 2024 Due Date December 16 2024 Description Quantity Unit Price Amount Web Development Services 40 150 6000 Subtotal 7200 Tax 612 Total 7812 Payment Terms Net 30",
        "INVOICE Number 2024-11-789 From Design Studio Pro To XYZ Enterprises Item Qty Rate Total Logo Design 1 2500 2500 Subtotal 4500 Sales Tax 384 Total Amount Due 4434",
        "TAX INVOICE 2024-Q4-5678 Vendor Tech Solutions Customer Global Systems Products Software License 12000 Subtotal 18500 Tax 1538 TOTAL DUE 20188",
        "BILLING STATEMENT Account 98765 Previous Balance 2500 Payments 2500 New Charges 3200 Current Balance 3200 Professional Services 40 hrs 80 3200 Due Date 11/30/2024",
        "RECEIPT Order 55443 Customer Tech Startup Items Website Hosting Premium 1200 SSL Certificate 100 Subtotal 1315 Total Paid 1341 Payment Visa 4567",
        
        # Additional invoice variations
        "PROFORMA INVOICE No PI-2024-556 Issued November 2024 Seller: Manufacturing Co Buyer: Retail Store Products Widget A Quantity 500 Unit Price 25 12500 Widget B Quantity 300 Unit Price 40 12000 Gross Total 24500 Discount 5 percent 1225 Net Total 23275 VAT 20 percent 4655 Grand Total 27930 Valid Until December 31 2024",
        "SALES INVOICE Invoice 78901 Date 11/15/2024 Sold To: Construction Company Description Hours Rate Amount Consulting Services 80 125 10000 Materials 5000 Equipment Rental 3000 Subtotal 18000 Sales Tax 8.5 percent 1530 Total Amount 19530 Payment Due 30 Days Terms Net 30",
        "MONTHLY INVOICE Account No 445566 Billing Period October 2024 Service Description Charges Internet Service 99.99 Phone Service 49.99 Cloud Storage 19.99 Total Current Charges 169.97 Previous Balance 0.00 Payments Received 0.00 Amount Due 169.97 Due Date November 30 2024",
        "COMMERCIAL INVOICE Invoice No CI-2024-8899 Exporter Import Export LLC Consignee Global Trading Corp Commodity Electronics Quantity 1000 units Value 50000 USD Freight Charges 2500 Insurance 500 Total Invoice Value 53000 Payment Terms Letter of Credit Incoterms FOB",
        "RENT INVOICE Tenant John Smith Property 123 Main St Apartment 4B Rent Period December 2024 Monthly Rent 2000 Parking Fee 100 Utilities 150 Late Fee 0 Total Amount Due 2250 Due Date December 1 2024 Payment Methods Check Direct Deposit",
        "CATERING INVOICE Event Wedding Reception Date November 20 2024 Items Guest Count 150 Cost per Person 75 Food Service 11250 Bar Service Open Bar 3500 Service Charge 15 percent 2213 Subtotal 16963 Gratuity 18 percent 3053 Total Amount 20016 Deposit Paid 5000 Balance Due 15016",
    ],
    
    'contract': [
        # Original contracts  
        "SERVICE AGREEMENT entered November 2024 BETWEEN Client ABC Corporation AND Service Provider Tech Solutions SCOPE OF SERVICES Web application development TERM twelve months COMPENSATION 50000 CONFIDENTIALITY TERMINATION 30 days GOVERNING LAW California",
        "EMPLOYMENT CONTRACT effective January 2025 BETWEEN Tech Innovations Employer AND Jane Smith Employee POSITION Senior Software Engineer COMPENSATION Salary 120000 Bonus 20 percent BENEFITS Health insurance 401k 20 days paid time NON-COMPETE 12 months",
        "NON-DISCLOSURE AGREEMENT between Company A Disclosing Party Company B Receiving Party Confidential Information trade secrets business plans customer data Obligations not disclose Term 3 years Remedies injunctive relief damages",
        "CONSULTING AGREEMENT Independent Contractor between Client XYZ Consultant ABC Services Strategic planning market analysis Compensation 10000 per month Term 6 months Intellectual Property work product belongs Client Termination 30 days notice",
        
        # Additional contract variations
        "LEASE AGREEMENT This Lease dated November 1 2024 BETWEEN Landlord Property Management LLC TENANT Sarah Williams PREMISES 456 Oak Street Unit 2B Term 12 months commencing December 1 2024 RENT 1800 monthly due first of month SECURITY DEPOSIT 3600 UTILITIES Tenant responsible electric gas PETS Not permitted MAINTENANCE Landlord responsible major repairs TERMINATION 60 days written notice",
        "PURCHASE AGREEMENT Agreement dated November 15 2024 SELLER Manufacturing Corp BUYER Distribution Inc GOODS Industrial Equipment Model X500 QUANTITY 50 units PRICE 5000 per unit Total 250000 DELIVERY FOB Seller warehouse within 30 days PAYMENT 50 percent deposit balance upon delivery WARRANTY 2 years parts labor GOVERNING LAW State of Texas",
        "PARTNERSHIP AGREEMENT Partners John Doe Jane Smith effective December 2024 BUSINESS NAME Tech Ventures LLC PURPOSE Software development consulting CAPITAL CONTRIBUTION John 100000 Jane 100000 PROFIT SHARING 50 percent each MANAGEMENT Decisions require unanimous consent DISSOLUTION Requires 60 days notice DISPUTE RESOLUTION Binding arbitration",
        "SOFTWARE LICENSE AGREEMENT Licensor Software Corp Licensee Business User GRANT OF LICENSE Non-exclusive non-transferable license TERM Perpetual FEES One-time 10000 annual maintenance 2000 RESTRICTIONS No reverse engineering No redistribution SUPPORT Email support business hours Updates included WARRANTY As-is LIMITATION OF LIABILITY Not exceed fees paid",
        "INDEPENDENT CONTRACTOR AGREEMENT Client Marketing Agency Contractor Freelance Designer SERVICES Graphic design brand identity DELIVERABLES Logo mockups Style guide TIMELINE 30 days PROJECT FEE 5000 milestone payments EXPENSES Reimbursable with receipts OWNERSHIP Client owns all work product CONFIDENTIALITY Non-disclosure required TERMINATION Either party 14 days notice",
        "FRANCHISE AGREEMENT Franchisor Restaurant Chain Inc Franchisee Owner Operator LLC GRANT Franchise to operate restaurant TERRITORY Exclusive rights City limits TERM 10 years renewable INITIAL FEE 50000 ROYALTY 6 percent gross sales TRAINING Required 4 weeks STANDARDS Must follow operating procedures TERMINATION Breach allows immediate termination",
    ],
    
    'letter': [
        # Original letters
        "Dear Mr Johnson I am writing to express sincere gratitude for interview opportunity Software Engineer position impressed by team innovative approach Thank you again Sincerely Sarah Williams",
        "Dear Valued Customer Subject Important Update Service Terms We hope this finds you well inform upcoming changes Enhanced security Expanded support hours New pricing We value your business Best regards Michael Chen",
        "Dear Hiring Manager excited to apply Marketing Director position 8 years experience digital marketing led campaigns generating 5M revenue expertise SEO SEM content strategy social media Please find resume attached Thank you Jennifer Martinez",
        "Dear Dr Smith Thank you for seeing me regarding annual physical appreciate thoroughness will schedule follow-up blood work make lifestyle changes discussed Looking forward next appointment Robert Johnson",
        
        # Additional letter variations
        "Dear Members Board of Directors I am pleased to present quarterly update operations Following successful product launch revenue exceeded projections by 15 percent Customer satisfaction remains high 92 percent Looking ahead expanding into new markets Respectfully submitted CEO Williams",
        "Dear Parents Welcome back to school year We are excited to begin another year learning growth This year introducing new STEM curriculum enhanced arts program Parent-teacher conferences scheduled October Please mark calendars Looking forward to wonderful year Principal Anderson Elementary School",
        "Dear Homeowner Association members This letter serves as notice upcoming special assessment roof repairs estimated cost 50000 divided among 25 units 2000 per unit Payment due January 15 2025 Board has obtained multiple bids selected qualified contractor Questions contact management office Sincerely HOA Board",
        "Dear Policy Holder This confirms receipt your claim number CL-2024-8899 filed November 10 2024 Adjuster will contact you within 3 business days inspect damage Please retain all receipts related repairs temporary housing Questions call claims department 800-555-0199 reference claim number Best regards Insurance Company Claims",
        "Dear Scholarship Committee I am writing to apply for merit scholarship academic year 2024-2025 Currently junior majoring Computer Science GPA 3.9 Active in student government volunteer tutoring program Financial assistance would allow me to continue studies without additional employment Attached find transcripts recommendation letters Thank you for consideration Sincerely Student Name",
        "Dear Colleague I wanted to personally reach out to inform you of my decision to resign from position Senior Manager effective December 31 2024 accepting opportunity Chief Operations Officer grateful for mentorship support over past 5 years wish continued success Happy to assist with transition Best wishes Former Manager Name",
    ],
    
    'report': [
        # Original reports
        "QUARTERLY BUSINESS REPORT Q4 2024 Executive Summary analysis company performance Financial Performance Revenue 12.5M Net Profit 2.3M Key Findings Customer acquisition increased 35 percent Market Analysis competitive landscape Recommendations Increase investment R&D Conclusion performance exceeded targets",
        "TECHNICAL ANALYSIS REPORT Cloud Migration Assessment Introduction findings comprehensive assessment Methodology Infrastructure audit Performance benchmarking Cost Analysis Current 850K Projected cloud 620K 27 percent savings Recommendations phased approach Conclusion significant cost savings improved scalability",
        "MONTHLY SALES REPORT October 2024 Total sales 450K 12 percent increase New customers 145 retention 92 percent Regional Performance North 180K East 135K West 90K South 45K Top Products A 125K B 98K C 87K Action Items Increase marketing Hire 2 sales reps Launch new product Q1",
        "INCIDENT REPORT IR-2024-1156 November 15 2024 Time 14:30 Location Building A fire alarm activated conference room 301 Building evacuated 5 minutes Fire department 14:38 Cause overheated projector No fire injuries Damage 2500 Recommendations Install sensors quarterly inspections Update evacuation procedures",
        
        # Additional report variations
        "ANNUAL PERFORMANCE REPORT Employee John Anderson Position Software Engineer Review Period January-December 2024 KEY ACCOMPLISHMENTS Delivered 8 major projects on time Led migration to microservices Mentored 3 junior developers PERFORMANCE RATINGS Technical Skills Excellent Communication Very Good Leadership Good GOALS 2025 Senior Engineer promotion Complete AWS certification Lead team of 5 OVERALL RATING Exceeds Expectations Recommended Salary Increase 8 percent",
        "MARKET RESEARCH REPORT Industry Smart Home Devices Date November 2024 EXECUTIVE SUMMARY Market size 95B growing 23 percent annually Major players Amazon Google Apple CONSUMER TRENDS Voice control most desired feature Security concerns remain Privacy priorities COMPETITIVE ANALYSIS Amazon leads 35 percent market share Google second 28 percent Apple third 18 percent RECOMMENDATIONS Focus on privacy features Integrate AI capabilities Expand product ecosystem",
        "PROJECT STATUS REPORT Project Website Redesign Status 65 percent complete Timeline On track Budget Under by 5K KEY MILESTONES Completed Design phase Development 80 percent Testing begins December RISKS Dependencies on third-party API Integration delays possible NEXT STEPS Complete backend development Begin user testing Prepare launch plan TEAM UPDATES Added 2 developers All team members meeting deadlines",
        "FINANCIAL AUDIT REPORT Company XYZ Corporation Audit Period Fiscal Year 2024 OPINION Financial statements present fairly material respects FINDINGS Internal controls adequate Revenue recognition appropriate Inventory valuation reasonable RECOMMENDATIONS Enhance documentation procedures Implement dual authorization Update accounting software MANAGEMENT RESPONSE Agrees with recommendations Implementation timeline 90 days AUDITOR Certified Public Accountants",
        "LABORATORY TEST REPORT Patient John Smith Date November 16 2024 Tests Ordered Complete Blood Count Lipid Panel Glucose RESULTS CBC Within normal ranges Cholesterol Total 195 LDL 115 HDL 55 Glucose Fasting 92 INTERPRETATION All values within normal limits No significant abnormalities detected RECOMMENDATIONS Continue current health regimen Retest in 12 months Physician Dr Sarah Johnson MD",
        "ENVIRONMENTAL IMPACT REPORT Project Commercial Development Site 123 Industrial Park SCOPE Air quality Water resources Wildlife habitat Traffic impact FINDINGS Minimal impact on air quality Storm water management adequate Protected species not present Traffic study shows acceptable levels MITIGATION MEASURES Install pollution controls Preserve 20 percent green space Create wildlife corridors CONCLUSION Project approved with conditions Public comment period 30 days",
    ],
}
