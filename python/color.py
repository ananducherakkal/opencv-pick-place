def get_color (r, g, b):
    if r > 1.2*b and r > 1.2*g:       
        return "red"
    if g > 1.2 * r and g > 1.2 * b:   
        return "green" 
    if b > 1.2 * r and b > 1.2 * g:      
        return "blue" 
    if r < 20 and g < 20 and b < 20:  # Checking if all values are low to classify as black
        return "black"