from hospital.validators import (
    validate_phone,
    validate_date,
    validate_positive_number,
    validate_required
)

print(validate_phone("9876543210"))
print(validate_phone("123"))

print(validate_date("2026-10-05"))
print(validate_date("05-10-2026"))

print(validate_positive_number("700"))
print(validate_positive_number("-100"))

print(validate_required("Divya"))
print(validate_required(""))