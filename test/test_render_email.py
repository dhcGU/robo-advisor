from app.robo_advisor import render_email

def test_render_email():
    html = "<div><br>"
    html += "<b>Alert!</b><br>"
    html += "AAPL\'s price has swung by 10.00% in the past day!<br>"
    html += "Search for AAPL with Robo Advisor for more information and a recommendation.<br>"
    html += "</div>"
    assert render_email("AAPL", 0.1) == html