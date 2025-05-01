def generate_post(trend):
    print(f"✍️ Drafting post about: {trend}")
    return f"# {trend}\n\nThis is an auto-generated post about {trend}."

if __name__ == "__main__":
    print(generate_post("Sample Tech Trend"))
