"""
Code Templates for Common Programming Problems
Provides instant code generation without API calls
"""

PYTHON_TEMPLATES = {
    "palindrome": '''def is_palindrome(text):
    """
    Check if a given string is a palindrome.

    A palindrome is a word, phrase, number, or other sequence of characters
    which reads the same backward as forward, ignoring spaces, punctuation,
    and capitalization.

    Args:
        text: The string to check.

    Returns:
        True if the string is a palindrome, False otherwise.
    """
    # Remove spaces and convert to lowercase for comparison
    processed_text = ''.join(char.lower() for char in text if char.isalnum())

    # Compare the processed text with its reverse
    return processed_text == processed_text[::-1]


# Example usage
if __name__ == "__main__":
    # Test cases
    print(f"'madam' is a palindrome: {is_palindrome('madam')}")  # Expected: True
    print(f"'A man, a plan, a canal: Panama' is a palindrome: {is_palindrome('A man, a plan, a canal: Panama')}")  # Expected: True
    print(f"'racecar' is a palindrome: {is_palindrome('racecar')}")  # Expected: True
    print(f"'hello' is a palindrome: {is_palindrome('hello')}")  # Expected: False
    print(f"'12321' is a palindrome: {is_palindrome('12321')}")  # Expected: True
''',

    "reverse_number": '''def reverse_number(num):
    """
    Reverse the digits of a number.

    Args:
        num: The number to reverse (can be positive or negative).

    Returns:
        The number with its digits reversed.
    """
    # Handle negative numbers
    is_negative = num < 0
    num = abs(num)

    # Reverse the number
    reversed_num = 0
    while num > 0:
        digit = num % 10
        reversed_num = reversed_num * 10 + digit
        num = num // 10

    # Apply the sign back
    return -reversed_num if is_negative else reversed_num


def reverse_number_string_method(num):
    """
    Alternative method: Reverse number using string manipulation.

    Args:
        num: The number to reverse.

    Returns:
        The reversed number.
    """
    # Convert to string, reverse, and convert back to integer
    is_negative = num < 0
    num_str = str(abs(num))
    reversed_str = num_str[::-1]
    reversed_num = int(reversed_str)

    return -reversed_num if is_negative else reversed_num


# Example usage
if __name__ == "__main__":
    # Test cases
    print(f"Reverse of 12345: {reverse_number(12345)}")  # Expected: 54321
    print(f"Reverse of -9876: {reverse_number(-9876)}")  # Expected: -6789
    print(f"Reverse of 100: {reverse_number(100)}")  # Expected: 1
    print(f"Reverse of 7: {reverse_number(7)}")  # Expected: 7

    # Using string method
    print(f"\\nUsing string method:")
    print(f"Reverse of 12345: {reverse_number_string_method(12345)}")  # Expected: 54321
''',

    "fibonacci": '''def fibonacci(n):
    """
    Generate Fibonacci sequence up to n terms.

    The Fibonacci sequence is: 0, 1, 1, 2, 3, 5, 8, 13, 21, ...
    Each number is the sum of the two preceding ones.

    Args:
        n: Number of terms to generate.

    Returns:
        List containing the Fibonacci sequence.
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    # Initialize the sequence
    fib_sequence = [0, 1]

    # Generate remaining terms
    for i in range(2, n):
        next_term = fib_sequence[i-1] + fib_sequence[i-2]
        fib_sequence.append(next_term)

    return fib_sequence


def fibonacci_recursive(n):
    """
    Calculate nth Fibonacci number using recursion.
    Note: This is less efficient for large n.

    Args:
        n: Position in Fibonacci sequence (0-indexed).

    Returns:
        The nth Fibonacci number.
    """
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)


# Example usage
if __name__ == "__main__":
    # Generate sequence
    print(f"First 10 Fibonacci numbers: {fibonacci(10)}")
    print(f"First 15 Fibonacci numbers: {fibonacci(15)}")

    # Individual terms
    print(f"\\n5th Fibonacci number: {fibonacci_recursive(5)}")
    print(f"10th Fibonacci number: {fibonacci_recursive(10)}")
''',

    "factorial": '''def factorial(n):
    """
    Calculate the factorial of a number.
    Factorial of n (n!) = n × (n-1) × (n-2) × ... × 1

    Args:
        n: Non-negative integer.

    Returns:
        The factorial of n.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    elif n == 0 or n == 1:
        return 1

    result = 1
    for i in range(2, n + 1):
        result *= i

    return result


def factorial_recursive(n):
    """
    Calculate factorial using recursion.

    Args:
        n: Non-negative integer.

    Returns:
        The factorial of n.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    elif n == 0 or n == 1:
        return 1

    return n * factorial_recursive(n - 1)


# Example usage
if __name__ == "__main__":
    # Test cases
    print(f"Factorial of 5: {factorial(5)}")  # Expected: 120
    print(f"Factorial of 7: {factorial(7)}")  # Expected: 5040
    print(f"Factorial of 0: {factorial(0)}")  # Expected: 1

    # Using recursive method
    print(f"\\nUsing recursion:")
    print(f"Factorial of 6: {factorial_recursive(6)}")  # Expected: 720
''',

    "prime": '''def is_prime(n):
    """
    Check if a number is prime.

    A prime number is a natural number greater than 1 that has no
    positive divisors other than 1 and itself.

    Args:
        n: The number to check.

    Returns:
        True if n is prime, False otherwise.
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Check odd divisors up to sqrt(n)
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2

    return True


def get_primes_up_to(limit):
    """
    Find all prime numbers up to a given limit using Sieve of Eratosthenes.

    Args:
        limit: Upper limit for finding primes.

    Returns:
        List of all prime numbers up to limit.
    """
    if limit < 2:
        return []

    # Create a boolean array and initialize all entries as true
    is_prime_array = [True] * (limit + 1)
    is_prime_array[0] = is_prime_array[1] = False

    # Sieve of Eratosthenes
    p = 2
    while p * p <= limit:
        if is_prime_array[p]:
            # Mark all multiples of p as not prime
            for i in range(p * p, limit + 1, p):
                is_prime_array[i] = False
        p += 1

    # Collect all prime numbers
    return [num for num in range(limit + 1) if is_prime_array[num]]


# Example usage
if __name__ == "__main__":
    # Test individual numbers
    print(f"Is 17 prime? {is_prime(17)}")  # Expected: True
    print(f"Is 25 prime? {is_prime(25)}")  # Expected: False
    print(f"Is 2 prime? {is_prime(2)}")  # Expected: True

    # Get all primes up to 50
    print(f"\\nPrime numbers up to 50: {get_primes_up_to(50)}")
''',

    "bubble_sort": '''def bubble_sort(arr):
    """
    Sort an array using the bubble sort algorithm.

    Bubble sort repeatedly steps through the list, compares adjacent elements,
    and swaps them if they are in the wrong order.

    Args:
        arr: List of comparable elements to sort.

    Returns:
        The sorted list.
    """
    # Create a copy to avoid modifying the original
    arr_copy = arr.copy()
    n = len(arr_copy)

    # Traverse through all array elements
    for i in range(n):
        # Flag to optimize: stop if no swaps occur
        swapped = False

        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # Swap if the element is greater than the next element
            if arr_copy[j] > arr_copy[j + 1]:
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                swapped = True

        # If no swapping occurred, array is already sorted
        if not swapped:
            break

    return arr_copy


# Example usage
if __name__ == "__main__":
    # Test cases
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original array: {test_array}")
    print(f"Sorted array: {bubble_sort(test_array)}")

    # Test with already sorted array
    sorted_array = [1, 2, 3, 4, 5]
    print(f"\\nAlready sorted: {sorted_array}")
    print(f"After sorting: {bubble_sort(sorted_array)}")

    # Test with reverse sorted array
    reverse_array = [9, 7, 5, 3, 1]
    print(f"\\nReverse sorted: {reverse_array}")
    print(f"After sorting: {bubble_sort(reverse_array)}")
''',

    "binary_search": '''def binary_search(arr, target):
    """
    Search for a target value in a sorted array using binary search.

    Binary search works by repeatedly dividing the search interval in half.
    Time complexity: O(log n)

    Args:
        arr: Sorted list of comparable elements.
        target: The value to search for.

    Returns:
        Index of target if found, -1 otherwise.
    """
    left = 0
    right = len(arr) - 1

    while left <= right:
        # Calculate middle index
        mid = (left + right) // 2

        # Check if target is at mid
        if arr[mid] == target:
            return mid

        # If target is greater, ignore left half
        elif arr[mid] < target:
            left = mid + 1

        # If target is smaller, ignore right half
        else:
            right = mid - 1

    # Target not found
    return -1


def binary_search_recursive(arr, target, left=0, right=None):
    """
    Recursive implementation of binary search.

    Args:
        arr: Sorted list of comparable elements.
        target: The value to search for.
        left: Left boundary of search range.
        right: Right boundary of search range.

    Returns:
        Index of target if found, -1 otherwise.
    """
    if right is None:
        right = len(arr) - 1

    # Base case: element not found
    if left > right:
        return -1

    mid = (left + right) // 2

    # Target found
    if arr[mid] == target:
        return mid

    # Search left half
    elif arr[mid] > target:
        return binary_search_recursive(arr, target, left, mid - 1)

    # Search right half
    else:
        return binary_search_recursive(arr, target, mid + 1, right)


# Example usage
if __name__ == "__main__":
    # Test array (must be sorted!)
    sorted_array = [2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78]

    # Test cases
    print(f"Array: {sorted_array}")
    print(f"Search for 23: Index {binary_search(sorted_array, 23)}")  # Expected: 5
    print(f"Search for 56: Index {binary_search(sorted_array, 56)}")  # Expected: 8
    print(f"Search for 100: Index {binary_search(sorted_array, 100)}")  # Expected: -1

    # Using recursive method
    print(f"\\nUsing recursion:")
    print(f"Search for 12: Index {binary_search_recursive(sorted_array, 12)}")  # Expected: 3
'''
}


def get_template_code(problem_keywords, language="python"):
    """
    Get template code for common programming problems.

    Args:
        problem_keywords: Description or keywords of the problem.
        language: Programming language (currently only Python supported).

    Returns:
        Template code if available, None otherwise.
    """
    if language.lower() != "python":
        return None

    keywords_lower = problem_keywords.lower()

    # Match problem to template
    if "palindrome" in keywords_lower:
        return PYTHON_TEMPLATES["palindrome"]

    elif "reverse" in keywords_lower and "number" in keywords_lower:
        return PYTHON_TEMPLATES["reverse_number"]

    elif "fibonacci" in keywords_lower or "fib" in keywords_lower:
        return PYTHON_TEMPLATES["fibonacci"]

    elif "factorial" in keywords_lower:
        return PYTHON_TEMPLATES["factorial"]

    elif "prime" in keywords_lower:
        return PYTHON_TEMPLATES["prime"]

    elif "bubble" in keywords_lower and "sort" in keywords_lower:
        return PYTHON_TEMPLATES["bubble_sort"]

    elif "binary" in keywords_lower and "search" in keywords_lower:
        return PYTHON_TEMPLATES["binary_search"]

    return None


def list_available_templates():
    """
    List all available code templates.

    Returns:
        List of available template names.
    """
    return list(PYTHON_TEMPLATES.keys())


"""
Letter Templates Module
Provides instant letter generation with customizable variables
"""

from datetime import datetime

LETTER_TEMPLATES = {
    "leave": {
        "name": "Leave Application Letter",
        "variables": ["sender_name", "recipient_name", "recipient_title", "organization", "leave_days", "leave_reason",
                      "start_date", "end_date"],
        "template": """Date: {date}

{recipient_name}
{recipient_title}
{organization}

Subject: Application for Leave

Respected {recipient_title},

I am writing to request leave from {start_date} to {end_date} ({leave_days} days) due to {leave_reason}.

I will ensure that all my pending work is completed before my leave, and I will be available for any urgent matters via phone or email if needed.

I kindly request you to grant me leave for the mentioned period. I will be grateful for your approval.

Thank you for your understanding and consideration.

Yours sincerely,
{sender_name}"""
    },

    "complaint": {
        "name": "Complaint Letter",
        "variables": ["sender_name", "sender_address", "recipient_name", "recipient_title", "organization",
                      "complaint_about", "issue_details", "expected_resolution"],
        "template": """Date: {date}

{sender_name}
{sender_address}

{recipient_name}
{recipient_title}
{organization}

Subject: Complaint Regarding {complaint_about}

Dear {recipient_title},

I am writing to bring to your attention a matter that requires immediate resolution regarding {complaint_about}.

{issue_details}

I would appreciate it if you could look into this matter and {expected_resolution}. I believe that a prompt response will help resolve this issue amicably.

I look forward to hearing from you soon and hope for a satisfactory resolution to this problem.

Thank you for your attention to this matter.

Sincerely,
{sender_name}"""
    },

    "appreciation": {
        "name": "Appreciation Letter",
        "variables": ["sender_name", "recipient_name", "appreciation_for", "specific_achievements", "impact"],
        "template": """Date: {date}

Dear {recipient_name},

I am writing to express my sincere appreciation for {appreciation_for}.

{specific_achievements}

Your dedication and efforts have made a significant impact: {impact}

Thank you once again for your outstanding contribution. Your work is truly valued and appreciated.

With warm regards,
{sender_name}"""
    },

    "recommendation": {
        "name": "Recommendation Letter",
        "variables": ["sender_name", "sender_title", "sender_organization", "candidate_name", "position_applied",
                      "relationship_duration", "key_skills", "achievements", "recommendation_statement"],
        "template": """Date: {date}

To Whom It May Concern,

I am writing to provide my highest recommendation for {candidate_name} for the position of {position_applied}.

I have known {candidate_name} for {relationship_duration} in my capacity as {sender_title} at {sender_organization}. During this time, I have been consistently impressed by their performance and character.

Key Skills and Qualities:
{key_skills}

Notable Achievements:
{achievements}

{recommendation_statement}

I am confident that {candidate_name} will be an excellent addition to your organization and will bring the same level of dedication and excellence that they have demonstrated while working with us.

Please feel free to contact me if you need any additional information.

Sincerely,
{sender_name}
{sender_title}
{sender_organization}"""
    },

    "resignation": {
        "name": "Resignation Letter",
        "variables": ["sender_name", "position", "recipient_name", "recipient_title", "organization",
                      "last_working_day", "reason", "gratitude_message"],
        "template": """Date: {date}

{recipient_name}
{recipient_title}
{organization}

Subject: Resignation from the Position of {position}

Dear {recipient_title},

I am writing to formally notify you of my resignation from the position of {position} at {organization}. My last working day will be {last_working_day}.

{reason}

I want to express my sincere gratitude for the opportunities I have been given during my time here. {gratitude_message}

I am committed to ensuring a smooth transition and will do everything possible to complete my current projects and assist in training my replacement.

Thank you once again for the opportunity to be part of this organization.

Yours sincerely,
{sender_name}"""
    },

    "invitation": {
        "name": "Invitation Letter",
        "variables": ["sender_name", "event_name", "event_date", "event_time", "event_location", "event_purpose",
                      "recipient_name", "rsvp_details"],
        "template": """Date: {date}

Dear {recipient_name},

It is my pleasure to invite you to {event_name}.

Event Details:
Date: {event_date}
Time: {event_time}
Location: {event_location}

Purpose: {event_purpose}

We would be honored by your presence at this event. Your attendance would mean a great deal to us.

{rsvp_details}

We look forward to seeing you there.

Warm regards,
{sender_name}"""
    },

    "apology": {
        "name": "Apology Letter",
        "variables": ["sender_name", "recipient_name", "what_happened", "impact", "corrective_actions", "commitment"],
        "template": """Date: {date}

Dear {recipient_name},

I am writing to sincerely apologize for {what_happened}.

I understand that this has {impact}, and I take full responsibility for my actions/oversight.

To rectify this situation, I have taken the following steps:
{corrective_actions}

{commitment}

I hope you can accept my sincere apology, and I am committed to ensuring that such incidents do not occur in the future.

Sincerely,
{sender_name}"""
    },

    "job_application": {
        "name": "Job Application Letter",
        "variables": ["sender_name", "sender_address", "sender_phone", "sender_email", "recipient_name",
                      "recipient_title", "organization", "position", "qualifications", "experience", "why_interested"],
        "template": """Date: {date}

{sender_name}
{sender_address}
Phone: {sender_phone}
Email: {sender_email}

{recipient_name}
{recipient_title}
{organization}

Subject: Application for the Position of {position}

Dear {recipient_title},

I am writing to express my interest in the {position} position at {organization}. I believe my qualifications and experience make me an ideal candidate for this role.

Qualifications:
{qualifications}

Experience:
{experience}

Why I am interested:
{why_interested}

I have attached my resume for your review. I would welcome the opportunity to discuss how my skills and experiences align with your needs.

Thank you for considering my application. I look forward to the opportunity to speak with you.

Sincerely,
{sender_name}"""
    },

    "thank_you": {
        "name": "Thank You Letter",
        "variables": ["sender_name", "recipient_name", "occasion", "what_received", "how_it_helped",
                      "closing_sentiment"],
        "template": """Date: {date}

Dear {recipient_name},

I wanted to take a moment to express my heartfelt thanks for {occasion}.

{what_received}

{how_it_helped}

{closing_sentiment}

Once again, thank you for your kindness and generosity.

With sincere gratitude,
{sender_name}"""
    },

    "permission": {
        "name": "Permission Request Letter",
        "variables": ["sender_name", "recipient_name", "recipient_title", "organization", "permission_for", "reason",
                      "duration", "benefits"],
        "template": """Date: {date}

{recipient_name}
{recipient_title}
{organization}

Subject: Request for Permission - {permission_for}

Respected {recipient_title},

I am writing to request your permission for {permission_for}.

Reason: {reason}

Duration: {duration}

Benefits: {benefits}

I assure you that I will adhere to all guidelines and regulations associated with this request. Your approval would be greatly appreciated.

Thank you for your time and consideration.

Respectfully,
{sender_name}"""
    },

    "inquiry": {
        "name": "Inquiry Letter",
        "variables": ["sender_name", "sender_organization", "recipient_name", "organization", "inquiry_about",
                      "specific_questions", "purpose", "deadline"],
        "template": """Date: {date}

{sender_name}
{sender_organization}

{recipient_name}
{organization}

Subject: Inquiry Regarding {inquiry_about}

Dear {recipient_name},

I am writing on behalf of {sender_organization} to inquire about {inquiry_about}.

Purpose: {purpose}

Specific Questions:
{specific_questions}

{deadline}

I would greatly appreciate your response at your earliest convenience. Please feel free to contact me if you need any additional information.

Thank you for your assistance.

Best regards,
{sender_name}
{sender_organization}"""
    },

    "reference": {
        "name": "Reference Request Letter",
        "variables": ["sender_name", "recipient_name", "relationship", "position_applying", "deadline", "why_chosen",
                      "contact_info"],
        "template": """Date: {date}

Dear {recipient_name},

I hope this letter finds you well. I am reaching out to ask if you would be willing to serve as a reference for me as I apply for {position_applying}.

{relationship}

{why_chosen}

The deadline for the reference is {deadline}. The potential employer may contact you at: {contact_info}

I would be happy to provide you with any additional information you might need. Thank you for considering my request.

Warm regards,
{sender_name}"""
    },

    "formal_general": {
        "name": "General Formal Letter",
        "variables": ["sender_name", "recipient_name", "recipient_title", "organization", "subject", "opening",
                      "main_content", "closing"],
        "template": """Date: {date}

{recipient_name}
{recipient_title}
{organization}

Subject: {subject}

Dear {recipient_title},

{opening}

{main_content}

{closing}

Thank you for your attention to this matter.

Sincerely,
{sender_name}"""
    }
}

DEFAULT_VALUES = {
    "sender_name": "Your Name",
    "recipient_name": "Recipient Name",
    "recipient_title": "Sir/Madam",
    "organization": "Organization Name",
    "date": datetime.now().strftime("%B %d, %Y"),
    "leave_days": "2",
    "leave_reason": "personal reasons",
    "start_date": "specify start date",
    "end_date": "specify end date",
    "sender_address": "Your Address",
    "complaint_about": "the issue",
    "issue_details": "Please provide detailed information about the issue.",
    "expected_resolution": "take appropriate action",
    "appreciation_for": "your excellent work",
    "specific_achievements": "Your recent contributions have been outstanding.",
    "impact": "Your efforts have positively influenced our team and results.",
    "sender_title": "Your Title",
    "sender_organization": "Your Organization",
    "candidate_name": "Candidate Name",
    "position_applied": "Position Title",
    "relationship_duration": "duration of relationship",
    "key_skills": "- Skill 1\n- Skill 2\n- Skill 3",
    "achievements": "- Achievement 1\n- Achievement 2",
    "recommendation_statement": "I strongly recommend this candidate without reservation.",
    "position": "Your Position",
    "last_working_day": "specify last working day",
    "reason": "I have accepted a new opportunity that aligns with my career goals.",
    "gratitude_message": "I have learned and grown tremendously during my tenure here.",
    "event_name": "Event Name",
    "event_date": "Event Date",
    "event_time": "Event Time",
    "event_location": "Event Location",
    "event_purpose": "Purpose of the event",
    "rsvp_details": "Please RSVP by [date] to [contact].",
    "what_happened": "the situation that occurred",
    "corrective_actions": "- Action 1\n- Action 2",
    "commitment": "I am committed to preventing similar issues in the future.",
    "sender_phone": "Your Phone Number",
    "sender_email": "your.email@example.com",
    "qualifications": "Your relevant qualifications",
    "experience": "Your relevant experience",
    "why_interested": "Your interest in the position and company",
    "occasion": "your kindness",
    "what_received": "The gift/help you provided was wonderful.",
    "how_it_helped": "It has made a significant positive difference.",
    "closing_sentiment": "Your thoughtfulness is deeply appreciated.",
    "permission_for": "activity or event",
    "duration": "specify duration",
    "benefits": "This will benefit both parties involved.",
    "inquiry_about": "product/service/information",
    "specific_questions": "1. Question 1\n2. Question 2",
    "purpose": "The purpose of this inquiry",
    "deadline": "Please respond by [date] if possible.",
    "relationship": "I have known you through [context] for [duration].",
    "position_applying": "position title",
    "why_chosen": "I believe you would provide an excellent reference given your knowledge of my work.",
    "contact_info": "your contact information",
    "subject": "Subject of the Letter",
    "opening": "I am writing to discuss an important matter.",
    "main_content": "Main content of your letter goes here.",
    "closing": "I appreciate your time and consideration."
}


def detect_letter_type(description: str) -> str:
    """Detect letter type from user description"""
    description_lower = description.lower()

    letter_keywords = {
        "leave": ["leave", "holiday", "vacation", "absent", "time off"],
        "complaint": ["complaint", "complain", "issue", "problem"],
        "appreciation": ["appreciation", "thank", "appreciate", "gratitude"],
        "recommendation": ["recommendation", "recommend", "reference letter"],
        "resignation": ["resignation", "resign", "quit", "leaving job"],
        "invitation": ["invitation", "invite", "event"],
        "apology": ["apology", "apologize", "sorry", "regret"],
        "job_application": ["job application", "apply", "applying for"],
        "thank_you": ["thank you", "thanks"],
        "permission": ["permission", "request permission", "allow"],
        "inquiry": ["inquiry", "inquire", "ask about", "question about"],
        "reference": ["reference request", "asking for reference"],
        "formal_general": ["formal letter", "general letter"]
    }

    for letter_type, keywords in letter_keywords.items():
        if any(keyword in description_lower for keyword in keywords):
            return letter_type

    return "formal_general"


def extract_custom_values(description: str) -> dict:
    """Extract custom values from user's natural language description"""
    custom_values = {}
    description_lower = description.lower()

    # Extract recipient title
    if "principal" in description_lower:
        custom_values["recipient_title"] = "Principal"
        custom_values["recipient_name"] = "Principal"
    elif "manager" in description_lower:
        custom_values["recipient_title"] = "Manager"
        custom_values["recipient_name"] = "Manager"
    elif "boss" in description_lower:
        custom_values["recipient_title"] = "Sir/Madam"
        custom_values["recipient_name"] = "Boss"
    elif "teacher" in description_lower:
        custom_values["recipient_title"] = "Teacher"
        custom_values["recipient_name"] = "Teacher"

    # Extract duration for leave
    import re
    days_match = re.search(r'(\d+)\s*days?', description_lower)
    if days_match:
        custom_values["leave_days"] = days_match.group(1)

    # Extract reason for leave
    if "sick" in description_lower:
        custom_values["leave_reason"] = "health reasons / sickness"
    elif "family" in description_lower:
        custom_values["leave_reason"] = "family emergency"
    elif "personal" in description_lower:
        custom_values["leave_reason"] = "personal reasons"
    elif "wedding" in description_lower:
        custom_values["leave_reason"] = "attending a wedding"
    elif "medical" in description_lower:
        custom_values["leave_reason"] = "medical appointment"

    return custom_values


def generate_letter(description: str, custom_values: dict = None) -> dict:
    """
    Generate a letter based on description

    Args:
        description: Natural language description of the letter needed
        custom_values: Dictionary of custom values to override defaults

    Returns:
        dict with letter content and metadata
    """
    letter_type = detect_letter_type(description)

    if letter_type not in LETTER_TEMPLATES:
        return {
            "success": False,
            "error": f"Letter type '{letter_type}' not found"
        }

    template_info = LETTER_TEMPLATES[letter_type]

    # Start with default values
    values = DEFAULT_VALUES.copy()

    # Extract values from description
    extracted_values = extract_custom_values(description)
    values.update(extracted_values)

    # Apply custom values if provided
    if custom_values:
        values.update(custom_values)

    # Generate the letter
    try:
        letter_content = template_info["template"].format(**values)

        return {
            "success": True,
            "letter": letter_content,
            "letter_type": letter_type,
            "letter_name": template_info["name"],
            "variables_used": template_info["variables"],
            "values": values,
            "description": description
        }
    except KeyError as e:
        return {
            "success": False,
            "error": f"Missing variable: {str(e)}"
        }


def list_letter_types():
    """List all available letter types"""
    return {
        letter_type: info["name"]
        for letter_type, info in LETTER_TEMPLATES.items()
    }


def get_letter_variables(letter_type: str) -> list:
    """Get required variables for a specific letter type"""
    if letter_type in LETTER_TEMPLATES:
        return LETTER_TEMPLATES[letter_type]["variables"]
    return []


def show_letter_preview(letter_type: str) -> str:
    """Show a preview of a letter type with default values"""
    if letter_type not in LETTER_TEMPLATES:
        return f"Letter type '{letter_type}' not found"

    template_info = LETTER_TEMPLATES[letter_type]
    preview = template_info["template"].format(**DEFAULT_VALUES)

    return f"=== {template_info['name']} Preview ===\n\n{preview}"


if __name__ == "__main__":
    # Test the letter generator
    print("Available Letter Types:")
    for lt, name in list_letter_types().items():
        print(f"  - {lt}: {name}")

    print("\n" + "=" * 60)
    print("Test: Generate a leave letter")
    print("=" * 60)

    result = generate_letter("write a letter to principal for 2 days leave")
    if result["success"]:
        print(result["letter"])
        print(f"\n✅ Letter type detected: {result['letter_type']}")
"""
AI Code Generator Module
Handles intelligent code generation for multiple programming languages
"""

import os
from google import genai
from google.genai import types

client = None


def get_client():
    """Get or initialize the Gemini client"""
    global client
    if client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        client = genai.Client(api_key=api_key)
    return client


LANGUAGE_TEMPLATES = {
    "python": {
        "extension": ".py",
        "comment_style": "#",
        "editor": "notepad" if os.name == "nt" else "gedit"
    },
    "javascript": {
        "extension": ".js",
        "comment_style": "//",
        "editor": "notepad" if os.name == "nt" else "gedit"
    },
    "java": {
        "extension": ".java",
        "comment_style": "//",
        "editor": "notepad" if os.name == "nt" else "gedit"
    },
    "c": {
        "extension": ".c",
        "comment_style": "//",
        "editor": "notepad" if os.name == "nt" else "gedit"
    },
    "cpp": {
        "extension": ".cpp",
        "comment_style": "//",
        "editor": "notepad" if os.name == "nt" else "gedit"
    },
    "csharp": {
        "extension": ".cs",
        "comment_style": "//",
        "editor": "notepad" if os.name == "nt" else "gedit"
    },
    "ruby": {
        "extension": ".rb",
        "comment_style": "#",
        "editor": "notepad" if os.name == "nt" else "gedit"
    },
    "go": {
        "extension": ".go",
        "comment_style": "//",
        "editor": "notepad" if os.name == "nt" else "gedit"
    },
    "html": {
        "extension": ".html",
        "comment_style": "<!--",
        "editor": "notepad" if os.name == "nt" else "gedit"
    },
    "css": {
        "extension": ".css",
        "comment_style": "/*",
        "editor": "notepad" if os.name == "nt" else "gedit"
    }
}


def is_letter_request(description: str) -> bool:
    """Check if the description is requesting a letter"""
    description_lower = description.lower()

    # Strong letter indicators
    strong_indicators = [
        "write a letter", "write letter", "draft a letter", "draft letter",
        "compose a letter", "compose letter"
    ]

    if any(indicator in description_lower for indicator in strong_indicators):
        return True

    # Check for letter-specific keywords (but only if "write" or "draft" is also present)
    if "write" in description_lower or "draft" in description_lower or "compose" in description_lower:
        letter_types = [
            "leave application", "leave letter",
            "resignation letter", "complaint letter",
            "invitation letter", "apology letter",
            "thank you letter", "appreciation letter",
            "recommendation letter", "permission letter",
            "inquiry letter", "reference letter",
            "job application letter"
        ]
        return any(letter_type in description_lower for letter_type in letter_types)

    return False


def detect_language_from_description(description: str) -> str:
    """Detect programming language from description"""
    description_lower = description.lower()

    language_keywords = {
        "python": ["python", "py", "django", "flask"],
        "javascript": ["javascript", "js", "node", "react", "vue"],
        "java": ["java"],
        "c": ["c programming", " c code"],
        "cpp": ["c++", "cpp"],
        "csharp": ["c#", "csharp"],
        "ruby": ["ruby", "rails"],
        "go": ["go", "golang"],
        "html": ["html", "webpage"],
        "css": ["css", "styling"]
    }

    for lang, keywords in language_keywords.items():
        if any(keyword in description_lower for keyword in keywords):
            return lang

    return "python"


def clean_code_output(code: str) -> str:
    """Remove markdown code blocks and clean up the output"""
    code = code.strip()

    if code.startswith("```"):
        lines = code.split("\n")

        if lines[0].strip().startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        code = "\n".join(lines)

    return code.strip()


def generate_code(description: str, language: str | None = None) -> dict:
    """
    Generate code using templates (fast) or Gemini AI (fallback)
    Also handles letter generation requests

    Args:
        description: What the code should do or letter to write
        language: Programming language (auto-detected if not provided)

    Returns:
        dict with code/letter, language, and metadata
    """
    # Check if this is a letter request
    if is_letter_request(description):
        letter_result = generate_letter(description)
        if letter_result["success"]:
            return {
                "success": True,
                "code": letter_result["letter"],
                "language": "text",
                "extension": ".txt",
                "editor": "notepad" if os.name == "nt" else "gedit",
                "description": description,
                "source": "letter_template",
                "letter_type": letter_result["letter_type"],
                "letter_name": letter_result["letter_name"]
            }

    if not language:
        language = detect_language_from_description(description)

    language = language.lower()

    language_info = LANGUAGE_TEMPLATES.get(language, {
        "extension": ".txt",
        "comment_style": "#",
        "editor": "notepad"
    })

    # Try to get template code first (instant, reliable)
    template_code = get_template_code(description, language)
    if template_code:
        return {
            "success": True,
            "code": template_code,
            "language": language,
            "extension": language_info["extension"],
            "editor": language_info["editor"],
            "description": description,
            "source": "template"
        }

    # Fall back to AI generation if no template available
    prompt = f"""You are an expert {language} programmer. Generate clean, well-documented code for the following task:

TASK: {description}

REQUIREMENTS:
1. Write COMPLETE, WORKING {language} code
2. Include detailed comments explaining the logic
3. Follow {language} best practices and conventions
4. Make the code beginner-friendly and educational
5. Include example usage or test cases where appropriate
6. DO NOT include any explanations before or after the code
7. DO NOT use markdown formatting (no ```)
8. ONLY return the raw code

Generate the {language} code now:"""

    # Try multiple models in order of preference
    models_to_try = [
        "gemini-2.5-flash",  # Latest stable model (2025)
        "gemini-2.0-flash-exp",  # Experimental fallback
        "gemini-1.5-flash",  # Legacy fallback
    ]

    last_error = None

    for model_name in models_to_try:
        try:
            api_client = get_client()
            response = api_client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                )
            )

            if response.text:
                code = clean_code_output(response.text)

                return {
                    "success": True,
                    "code": code,
                    "language": language,
                    "extension": language_info["extension"],
                    "editor": language_info["editor"],
                    "description": description,
                    "source": "ai",
                    "model": model_name
                }

        except Exception as e:
            last_error = str(e)
            # If 404 or model not found, try next model
            if "404" in str(e) or "not found" in str(e).lower():
                continue
            else:
                # For other errors, don't try other models
                break

    # All models failed
    return {
        "success": False,
        "error": last_error or "All models failed",
        "code": f"# Error generating code: {last_error}\n# Try one of these templates: {', '.join(list_available_templates())}"
    }


def generate_multiple_versions(description: str, language: str | None = None, count: int = 1) -> list:
    """Generate multiple versions of code for comparison"""
    versions = []

    for i in range(count):
        result = generate_code(description, language)
        if result["success"]:
            versions.append(result)

    return versions


def explain_code(code: str, language: str = "python") -> str:
    """Generate explanation for existing code"""
    prompt = f"""Explain the following {language} code in simple terms:

{code}

Provide a clear, beginner-friendly explanation of:
1. What the code does
2. How it works (step by step)
3. Key concepts used"""

    models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash-exp", "gemini-1.5-flash"]

    for model_name in models_to_try:
        try:
            api_client = get_client()
            response = api_client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text or "Could not generate explanation"
        except Exception as e:
            if "404" in str(e) or "not found" in str(e).lower():
                continue
            return f"Error: {str(e)}"

    return "Error: All models failed to generate explanation"


def improve_code(code: str, language: str = "python") -> dict:
    """Suggest improvements for existing code"""
    prompt = f"""Analyze this {language} code and provide an improved version:

{code}

Improvements to make:
1. Better performance
2. More readable
3. Better error handling
4. Follow best practices
5. Add helpful comments

Return ONLY the improved code, no explanations."""

    models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash-exp", "gemini-1.5-flash"]

    for model_name in models_to_try:
        try:
            api_client = get_client()
            response = api_client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            if response.text:
                improved_code = clean_code_output(response.text)
                return {
                    "success": True,
                    "code": improved_code,
                    "language": language,
                    "model": model_name
                }
        except Exception as e:
            if "404" in str(e) or "not found" in str(e).lower():
                continue
            return {
                "success": False,
                "error": str(e)
            }

    return {
        "success": False,
        "error": "All models failed to improve code"
    }


def debug_code(code: str, error_message: str, language: str = "python") -> dict:
    """Debug code and fix errors"""
    prompt = f"""Fix the following {language} code that has this error:

ERROR: {error_message}

CODE:
{code}

Provide the corrected code with the bug fixed. Return ONLY the fixed code."""

    models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash-exp", "gemini-1.5-flash"]

    for model_name in models_to_try:
        try:
            api_client = get_client()
            response = api_client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            if response.text:
                fixed_code = clean_code_output(response.text)
                return {
                    "success": True,
                    "code": fixed_code,
                    "language": language,
                    "model": model_name
                }
        except Exception as e:
            if "404" in str(e) or "not found" in str(e).lower():
                continue
            return {
                "success": False,
                "error": str(e)
            }

    return {
        "success": False,
        "error": "All models failed to debug code"
    }
