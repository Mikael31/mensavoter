# Mensavoter - TUM Cafeteria Voting System

A web-based voting and information system for Technical University of Munich (TUM) cafeterias, featuring QR code navigation, menu displays, and interactive voting functionality.

## 🍽️ Overview

Mensavoter is a comprehensive web application that allows TUM students and staff to:
- View current menus for different TUM cafeterias
- Vote for their preferred cafeteria
- Navigate between different locations using QR codes
- View an interactive map of cafeteria locations

## 🏗️ Project Structure

```
mensavoter/
├── 📁 display/           # HTML pages for menu display and map
├── 📁 votes/             # Voting system backend
├── 📁 jsonpasser/        # Menu data fetching and processing
├── 📁 qrcodes/           # QR code images for navigation
├── 📁 waitqr/            # QR code callback handling (CPEE integration)
├── 📁 styles/            # CSS styling
├── 📁 pictures/          # Background images and assets
└── 📄 README.md          # This documentation
```

## 🎯 Features

### 1. Interactive Map
- **File**: `display/map.html`
- Interactive map showing TUM cafeteria locations
- Uses MapTiler SDK for mapping functionality
- Responsive design with TUM branding

### 2. Menu Display Pages
- **Files**: `display/mensa*.html`
- Individual pages for each cafeteria:
  - Mensa Garching (`mensagarching.html`)
  - Mensa Boltzmann (`mensabolzmann.html`) 
  - Mensa Maschinenbau (`mensamaschinenbau.html`)
- Real-time menu data from TUM Eat API
- QR code navigation between locations

### 3. Voting System
- **Directory**: `votes/`
- **Main File**: `vote.php`
- Vote counting for three cafeterias
- JSON-based data persistence
- Vote reset functionality

### 4. Menu Data Management
- **Directory**: `jsonpasser/`
- Fetches current week's menu data from TUM Eat API
- Filters menus to show only current day
- Separate endpoints for each cafeteria

### 5. QR Code Navigation
- **Directory**: `qrcodes/`
- Pre-generated QR codes for each location
- Enables easy navigation between different views
- Integration with CPEE workflow system

## 🚀 Setup Instructions

### Prerequisites
- Web server with PHP support (PHP 7.0+)
- Internet connection for menu data fetching
- Optional: MapTiler API key for enhanced mapping

### Installation

1. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   cd mensavoter
   ```

2. **Web Server Setup**:
   - Place the project directory in your web server's document root
   - Ensure PHP is enabled and configured
   - Make sure the `votes/data/` and `jsonpasser/data/` directories are writable

3. **MapTiler Configuration** (Optional):
   - Get a free API key from [MapTiler](https://maptiler.com)
   - Replace `KEY` in `display/map.html` line 142 with your API key

4. **Directory Permissions**:
   ```bash
   chmod 755 votes/data jsonpasser/data
   chmod 644 votes/data/* jsonpasser/data/*
   ```

### Quick Start

1. **Access the main map page**:
   ```
   http://your-domain/mensavoter/display/map.html
   ```

2. **View individual cafeteria menus**:
   ```
   http://your-domain/mensavoter/display/mensagarching.html
   http://your-domain/mensavoter/display/mensabolzmann.html
   http://your-domain/mensavoter/display/mensamaschinenbau.html
   ```

3. **Test voting functionality**:
   ```
   http://your-domain/mensavoter/votes/vote.php?mensa=mensa_garching
   ```

## 🔧 API Endpoints

### Voting API
- **Vote**: `GET /votes/vote.php?mensa={mensa_name}`
  - Parameters: `mensa` (mensa_garching, mensa_bolzmann, mensa_maschinenbau)
  - Response: JSON with success status and current vote counts

- **Reset Votes**: `GET /votes/reset_votes.php`
  - Resets all vote counts to zero

### Menu Data API
- **Fetch Menu Data**: `GET|POST /jsonpasser/{mensa_file}.php`
  - Available endpoints:
    - `/jsonpasser/index.php` - Generic menu fetcher
    - `/jsonpasser/mensa_garching.php` - Garching-specific
    - `/jsonpasser/mensa_bolzmann.php` - Boltzmann-specific
    - `/jsonpasser/mensa_maschinenbau.py` - Maschinenbau-specific
  - Parameters: 
    - `year` (optional): ISO year
    - `week` (optional): ISO week number
  - Response: JSON menu data for the specified week

### CPEE Integration
- **QR Callback**: `/waitqr/intiate.php`
  - Handles CPEE workflow callbacks
  - Stores callback URLs for process continuation

## 📱 QR Code System

The application uses QR codes for seamless navigation between different views:

- **Map QR Code** (`qrcodes/map.png`): Links to main map page
- **Cafeteria QR Codes**: Individual codes for each cafeteria
  - `qrcodes/mensagarching.png`
  - `qrcodes/mensabolzmann.png` 
  - `qrcodes/maschinenbau.png`
- **Voting QR Codes**: Enable direct voting functionality

## 🎨 Styling and Design

- **CSS Framework**: Custom CSS with TUM branding
- **Color Scheme**: TUM Blue (#3070b3) primary colors
- **Responsive Design**: Mobile-friendly layouts
- **Background Images**: TUM campus imagery
- **Typography**: System fonts with professional styling

## 📊 Data Sources

### TUM Eat API
- **Base URL**: `https://tum-dev.github.io/eat-api/`
- **Format**: Weekly JSON files with menu data
- **Structure**: Organized by cafeteria, year, and week
- **Update Frequency**: Weekly

### Local Data Storage
- **Vote Data**: `votes/data/votes.json`
- **Menu Cache**: `jsonpasser/data/*.json`
- **Format**: JSON with UTF-8 encoding

## 🔍 Supported Cafeterias

1. **Mensa Garching**
   - Location: Boltzmannstr. 19, 85748 Garching
   - API Endpoint: `mensa-garching`

2. **Mensa Boltzmann** 
   - Location: TUM Campus
   - API Endpoint: `mensa-boltzmann`

3. **Mensa Maschinenbau**
   - Location: TUM Campus
   - API Endpoint: `mensa-maschinenbau`

## 🛠️ Development Notes

### File Structure Details
- **HTML Pages**: Use semantic markup with accessibility considerations
- **PHP Scripts**: PHP 7.0+ compatible, error handling included
- **JSON Data**: Pretty-printed with Unicode support
- **CSS**: Modular structure with CSS custom properties

### Error Handling
- Network failures gracefully handled with fallback messages
- Invalid requests return appropriate HTTP status codes
- File operation errors logged and reported

### Performance Considerations
- Menu data cached locally to reduce API calls
- Optimized images and assets
- Efficient JSON processing
- Minimal external dependencies

## 📝 License

This project is part of the TUM ecosystem and follows university guidelines for student projects.

## 🤝 Contributing

For improvements or bug fixes:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For technical issues or questions related to this project, please refer to the TUM development community or create an issue in the project repository.

---

*Last updated: December 2024*
*Project Type: Web Application*
*Technologies: PHP, HTML5, CSS3, JavaScript, MapTiler SDK*
