

def set_salestax(request, tax_type, tax_total):
    """
    Stores the tax type and total in the session.
    """
    request.session["tax_type"] = tax_type
    request.session["tax_total"] = tax_total
