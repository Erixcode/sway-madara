# what included:
This is based on Fedora-sway Spin, for default packages installed, please visit Fedora42 Sway-Spin Docs : <url>https://fedoraproject.org/spins/sway</url>

     tmux plugins  --> needs to install tpm and run the install_plugins.sh script if failed just remove the folders inside plugins and relaunch the script
    .tmux.conf
    .bashrc
    .config/kitty
    .config/waybar
    .config/sway
    .config/wofi
    .config/rofi
    .local/bin/  --> I use wofi for application launching also the fedora logo at mid top bar works the same, for custom scripts like fzfind or fzps including my fzbmark.py I use rofi, you can Add any scripts there
for live background we need to download and compile mpvpaper: https://github.com/GhostNaN/mpvpaper


keybindings are based on my Own preferals, Most Commons:

     Super+D --> rofi (as custom Script launcher)
     Super+r --> wofi (as application launcher)
     Super+l --> swaylock
     Super+E --> nautilus
     Super+q --> exit apps
     Super+shift+s --> ScreenShot
     Super+Shit+number --> move to Desktop
     Super+number --> go to Desktop
     Super+f --> FullScreen/exit FullScreen
     Ctrl+Alt+Delete --> Logout
     Super+Shift+r --> reload sway (be careful about mpvpaper not eat your RAM)

for laptops with nvidia integrated Cards, do not use sway-nvidia it's old and will break:

    switch to a different TTY (Ctrl+Alt+F3).

    Log in and run:

    sudo systemctl stop display-manager  # Stops GDM/GNOME
    sudo modprobe -r nvidia_drm nvidia_modeset nvidia_uvm nvidia
    sway

    After exiting Sway:

    sudo modprobe nvidia_drm nvidia_modeset nvidia_uvm nvidia
    sudo systemctl start display-manager  # Restarts GNOME

Need to install GitHub repos:

    git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

    git clone --single-branch https://github.com/GhostNaN/mpvpaper
    # Build
    cd mpvpaper
    meson setup build --prefix=/usr/local
    ninja -C build
    # Install
    ninja -C build install

    https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/3270.zip
    https://github.com/subframe7536/maple-font/releases
    gsettings set org.gnome.desktop.interface gtk-theme "Adwaita-dark"
     
packages I installed via DNF are listed here:
    
    sudo dnf install qt5ct sway waybar meson git cmake gcc-c++ power-profiles-daemon mpv-devel wayland-devel wlroots-devel nautilus sway-wallpapers swayidle swaybg swayimg swaylock swappy slurp grim grimpicker fontawesome-fonts-all xclip fuzzel highlight wofi rofi fzf 
    pip install pygments

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/862d9213-ddfd-4ef4-a811-15cd916908fd" />

<img width="1919" height="1080" alt="image" src="https://github.com/user-attachments/assets/6e7de62b-7d1a-4980-a9ac-685f748425e2" />
    
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/453f16aa-c08a-4e0d-88c3-452512fd02b4" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1ffc2de2-87d6-4f2d-b6e8-2d0c015157a5" />

check Art.md to get the background video and swaylock image, for background video if you have a nice hardware go with 4k if not use HD version :)<br>


I didn't add dual monitor settings because it will change from system to system, Also I don't like tweaking gtk themes so much, "Adwaita-dark" is the only tweak I do, If you like you can also get it done via dconf-editor and other tools.<br>


for firefox I use <url>https://addons.mozilla.org/en-US/firefox/addon/apng-madara-uchiha/?utm_source=addons.mozilla.org&utm_medium=referral&utm_content=search</url> to mach the theme, this one I do manualy and not included in the rice.<br>
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/32c4b8fd-aa7f-4d79-9c89-abb5b8fd1ab9" />


Terminal also has few tricks:

     Ctrl+t --> fuzyfind 
     Ctrl+r --> fuzy history search
     Alt+c --> cd into folder of fuzy search results 
     cats --> bat implementation via python and highlight 

Peace :)<br>
My initial design was not as smooth as this rice, I got inspiration of <a href=https://github.com/diinki>diinki's</a> rice to give some soul to this rice :), if you want to go deep with customization I strongly advise to check her github page :)
