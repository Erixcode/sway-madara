#!/usr/bin/env python3
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any
import argparse

class BrowserBookmarkManager:
    def __init__(self):
        self.browser_profiles = self.detect_browser_profiles()
    
    def detect_browser_profiles(self) -> Dict[str, List[str]]:
        """Find browser bookmark files with manual configuration option"""
        profiles = {}
        
        # =====================================================================
        # MANUAL CONFIGURATION SECTION - Add your browser paths here if not auto-detected
        # =====================================================================
        
        # Firefox - auto detection
        firefox_path = Path.home() / '.mozilla' / 'firefox'
        if firefox_path.exists():
            firefox_dbs = []
            for profile_dir in firefox_path.iterdir():
                if profile_dir.is_dir() and not profile_dir.name.startswith('.'):
                    places_db = profile_dir / 'places.sqlite'
                    if places_db.exists() and places_db.stat().st_size > 0:
                        firefox_dbs.append(str(places_db))
            
            if firefox_dbs:
                profiles['firefox'] = firefox_dbs
        
        # Chrome/Chromium/Brave - auto detection
        chromium_browsers = {
            'chrome': '~/.config/google-chrome',
            'chromium': '~/.config/chromium', 
            'brave': '~/.config/BraveSoftware/Brave-Browser'
        }
        
        for browser, path in chromium_browsers.items():
            config_path = Path(path).expanduser()
            if config_path.exists():
                bookmark_files = []
                for entry in config_path.iterdir():
                    if entry.is_dir() and not entry.name.startswith('.'):
                        bookmark_file = entry / 'Bookmarks'
                        if bookmark_file.exists():
                            bookmark_files.append(str(bookmark_file))
                
                if bookmark_files:
                    profiles[browser] = bookmark_files
        
        # =====================================================================
        # MANUAL PATH OVERRIDES - Add your specific paths below this line
        # =====================================================================
        
        # Example manual configurations (uncomment and modify as needed):
        
        # # Firefox manual path (if auto-detection fails)
        # firefox_manual_path = "~/.mozilla/firefox/your_profile/places.sqlite"
        # expanded_path = Path(firefox_manual_path).expanduser()
        # if expanded_path.exists():
        #     profiles.setdefault('firefox', []).append(str(expanded_path))
        
        # # Chrome manual path (if auto-detection fails)
        # chrome_manual_path = "~/.config/google-chrome/Default/Bookmarks"
        # expanded_path = Path(chrome_manual_path).expanduser()
        # if expanded_path.exists():
        #     profiles.setdefault('chrome', []).append(str(expanded_path))
        
        # # Chromium manual path
        # chromium_manual_path = "~/.config/chromium/Default/Bookmarks"
        # expanded_path = Path(chromium_manual_path).expanduser()
        # if expanded_path.exists():
        #     profiles.setdefault('chromium', []).append(str(expanded_path))
        
        # # Brave manual path  
        # brave_manual_path = "~/.config/BraveSoftware/Brave-Browser/Default/Bookmarks"
        # expanded_path = Path(brave_manual_path).expanduser()
        # if expanded_path.exists():
        #     profiles.setdefault('brave', []).append(str(expanded_path))
        
        # # Flatpak browsers
        # flatpak_paths = {
        #     'chrome': '~/.var/app/com.google.Chrome/config/google-chrome/Default/Bookmarks',
        #     'chromium': '~/.var/app/org.chromium.Chromium/config/chromium/Default/Bookmarks',
        #     'brave': '~/.var/app/com.brave.Browser/config/BraveSoftware/Brave-Browser/Default/Bookmarks'
        # }
        # for browser, path in flatpak_paths.items():
        #     expanded_path = Path(path).expanduser()
        #     if expanded_path.exists():
        #         profiles.setdefault(browser, []).append(str(expanded_path))
        
        return profiles
    
    def parse_firefox_bookmarks(self, db_path: str) -> List[Dict[str, str]]:
        """Parse Firefox SQLite bookmarks"""
        bookmarks = []
        try:
            # Use URI mode with read-only to avoid locking issues
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            cursor = conn.execute("""
                SELECT moz_places.url, moz_bookmarks.title 
                FROM moz_places 
                JOIN moz_bookmarks ON moz_places.id = moz_bookmarks.fk
                WHERE moz_bookmarks.type = 1 
                AND moz_places.url IS NOT NULL
                AND moz_places.url LIKE 'http%'
            """)
            
            for url, title in cursor:
                bookmarks.append({
                    'url': url,
                    'title': title or url,
                    'source': 'firefox'
                })
            
            conn.close()
            
        except sqlite3.Error as e:
            print(f"Error reading Firefox bookmarks from {db_path}: {e}", file=sys.stderr)
        
        return bookmarks
    
    def parse_chromium_bookmarks(self, json_path: str, browser: str) -> List[Dict[str, str]]:
        """Parse Chrome/Chromium/Brave JSON bookmarks"""
        bookmarks = []
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            def extract_from_node(node: Dict[str, Any], folder: str = "") -> None:
                if 'children' in node:
                    current_folder = f"{folder}/{node.get('name', '')}".strip('/')
                    for child in node['children']:
                        extract_from_node(child, current_folder)
                elif node.get('type') == 'url' and 'url' in node:
                    url = node['url']
                    if url.startswith(('http://', 'https://')):
                        bookmarks.append({
                            'url': url,
                            'title': node.get('name', url),
                            'source': browser,
                            'folder': folder
                        })
            
            if 'roots' in data:
                for root_name, root_node in data['roots'].items():
                    if isinstance(root_node, dict):
                        extract_from_node(root_node, root_name)
                        
        except (json.JSONDecodeError, IOError, UnicodeDecodeError) as e:
            print(f"Error reading {browser} bookmarks from {json_path}: {e}", file=sys.stderr)
        
        return bookmarks
    
    def get_all_bookmarks(self, specific_browser: str = None) -> List[Dict[str, str]]:
        """Get all bookmarks from detected browsers"""
        all_bookmarks = []
        
        for browser, paths in self.browser_profiles.items():
            if specific_browser and browser != specific_browser:
                continue
                
            for path in paths:
                if browser == 'firefox':
                    all_bookmarks.extend(self.parse_firefox_bookmarks(path))
                else:
                    all_bookmarks.extend(self.parse_chromium_bookmarks(path, browser))
        
        return all_bookmarks
    
    def open_url(self, url: str, browser: str = None):
        """Open URL in appropriate browser"""
        try:
            if browser:
                subprocess.Popen([browser, url], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
            else:
                subprocess.Popen(['xdg-open', url], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"Error opening browser: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Terminal Browser Bookmark Manager")
    parser.add_argument("--browser", help="Use specific browser's bookmarks")
    parser.add_argument("--list-browsers", action='store_true', 
                       help="List detected browsers with bookmarks")
    parser.add_argument("--list", action='store_true', 
                       help="List all bookmarks without opening")
    parser.add_argument("--search", help="Search term (shows matching bookmarks)")
    parser.add_argument("--debug", action='store_true', 
                       help="Show debug information")
    
    args = parser.parse_args()
    manager = BrowserBookmarkManager()
    
    if args.list_browsers:
        print("Detected browsers with bookmarks:")
        if not manager.browser_profiles:
            print("  None detected automatically")
            print("\nTo add manual paths, edit the script and look for:")
            print("  'MANUAL PATH OVERRIDES' section")
        else:
            for browser, paths in manager.browser_profiles.items():
                print(f"  {browser}: {len(paths)} profile(s)")
                for path in paths:
                    print(f"    - {path}")
        return
    
    bookmarks = manager.get_all_bookmarks(args.browser)
    
    if not bookmarks:
        print("No bookmarks found in any browser!")
        print("\nIf browsers are not auto-detected:")
        print("1. Run with --list-browsers to see what was detected")
        print("2. Edit the script and add manual paths in the 'MANUAL PATH OVERRIDES' section")
        print("3. Common manual paths to try:")
        print("   - Firefox: ~/.mozilla/firefox/*/places.sqlite")
        print("   - Chrome: ~/.config/google-chrome/*/Bookmarks")
        print("   - Chromium: ~/.config/chromium/*/Bookmarks")
        return
    
    if args.list:
        for i, bm in enumerate(bookmarks, 1):
            folder_info = f" [{bm.get('folder', '')}]" if bm.get('folder') else ""
            print(f"{i:4d}. {bm['title'][:60]:60} | {bm['source']}{folder_info}")
            if args.debug:
                print(f"     {bm['url']}")
        return
    
    if args.search:
        search_lower = args.search.lower()
        filtered = [
            bm for bm in bookmarks 
            if (search_lower in bm['title'].lower() or 
                search_lower in bm['url'].lower() or
                search_lower in bm.get('folder', '').lower())
        ]
        
        if not filtered:
            print(f"No bookmarks found matching '{args.search}'")
            return
            
        print(f"Found {len(filtered)} bookmarks matching '{args.search}':")
        for i, bm in enumerate(filtered, 1):
            folder_info = f" [{bm.get('folder', '')}]" if bm.get('folder') else ""
            print(f"{i:3d}. {bm['title']} ({bm['source']}{folder_info})")
        
        try:
            choice = input("\nSelect bookmark number (or Enter to cancel): ").strip()
            if choice and choice.isdigit():
                selected = filtered[int(choice) - 1]
                browser_cmd = selected['source'] if selected['source'] != 'firefox' else 'firefox'
                manager.open_url(selected['url'], browser_cmd)
        except (ValueError, IndexError):
            print("Invalid selection")
        return
    
    # Interactive mode with fzf
    try:
        # Prepare input for fzf
        fzf_input = "\n".join(
            f"{bm['title']} | {bm['url']} | {bm['source']} | {bm.get('folder', '')}" 
            for bm in bookmarks
        )
        
        # Run fzf
        result = subprocess.run([
            'fzf', 
            '--delimiter', '|', 
            '--with-nth', '1,3,4',  # Show title, source, and folder
            '--preview', 'echo "URL: {2}\nFolder: {4}"', 
            '--preview-window', 'down:2:wrap'
        ], input=fzf_input, text=True, capture_output=True)
        
        if result.returncode == 0 and result.stdout.strip():
            selected_line = result.stdout.strip()
            parts = selected_line.split('|')
            if len(parts) >= 2:
                selected_url = parts[1].strip()
                selected_source = parts[2].strip() if len(parts) > 2 else ''
                
                # Determine browser command
                browser_cmd = None
                if selected_source == 'firefox':
                    browser_cmd = 'firefox'
                elif selected_source in ['chrome', 'chromium', 'brave']:
                    browser_cmd = selected_source
                
                manager.open_url(selected_url, browser_cmd)
            
    except FileNotFoundError:
        print("Error: fzf not found. Please install fzf to use interactive mode.")
        print("You can use --search or --list options instead.")

if __name__ == "__main__":
    main()
