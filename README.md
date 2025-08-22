# what included:
As I use Fedora-sway Spin some packages are installed by Default like rofi,...

    tmux plugins
    .tmux.conf
    .bashrc
    .config/nvim
    .config/geany
    .config/kitty
    .config/waybar
    .config/sway
    .config/wofi
    .config/rofi
    .local/bin/  --> for wofi custom launcher, need to bind new key for this mode, includes my fzbmark.py
for sway and waybar we need to download and compile mpvpaper: https://github.com/GhostNaN/mpvpaper
check deepseek session for package dependencies

for laptops with nvidia integrated Cards, do not use sway-nvidia it's old and will break:

    witch to a different TTY (Ctrl+Alt+F3).

    Log in and run:

    sudo systemctl stop display-manager  # Stops GDM/GNOME
    sudo modprobe -r nvidia_drm nvidia_modeset nvidia_uvm nvidia
    sway

    After exiting Sway:
    bash

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
    
    sudo dnf install qt5ct sway waybar meson git cmake gcc-c++ power-profiles-daemon mpv-devel wayland-devel wlroots-devel nautilus sway-wallpapers swayidle swaybg swayimg swaylock swappy slurp grim grimpicker fontawesome-fonts-all xclip fuzzel highlight wofi rofi
    pip install pygments
    
