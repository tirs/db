#!/usr/bin/env python3
"""
Start the Nutrition Database Web Server
Access at: http://localhost:5000
"""

from app import app

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║   🥗 NUTRITION DATABASE WEB DASHBOARD                         ║
    ║                                                                ║
    ║   Server Starting...                                          ║
    ║   Access at: http://localhost:5000                           ║
    ║                                                                ║
    ║   📊 Features:                                                 ║
    ║   • Search & filter foods by name or category                ║
    ║   • View detailed nutrition facts                            ║
    ║   • Export data to CSV                                        ║
    ║   • Interactive charts & analysis                            ║
    ║   • Browse by food category                                  ║
    ║   • Top foods by metrics                                     ║
    ║                                                                ║
    ║   Press Ctrl+C to stop the server                            ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    app.run(debug=False, host='0.0.0.0', port=5000)