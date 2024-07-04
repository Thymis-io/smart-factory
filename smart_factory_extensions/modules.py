from thymis_controller import models, modules


class Kiosk(modules.Module):
    displayName: str = "Kiosk Smart Factory"

    kiosk_url = models.Setting(
        name="kiosk.url",
        type="string",
        default="https://example.com",
        description="The URL to display in kiosk mode.",
        example="https://example.com",
    )

    resolution = models.Setting(
        name="kiosk.resolution",
        type="string",
        default="1920x1080",
        description="The resolution of the display.",
        example="1920x1080",
    )

    rotation = models.Setting(
        name="kiosk.rotation",
        type="string",
        default="normal",
        description="The rotation of the display.",
        example="normal",
    )

    def write_nix_settings(
        self, f, module_settings: models.ModuleSettings, priority: int
    ):
        kiosk_url = (
            module_settings.settings["kiosk_url"]
            if "kiosk_url" in module_settings.settings
            else self.kiosk_url.default
        )

        resolution = (
            module_settings.settings["resolution"]
            if "resolution" in module_settings.settings
            else self.resolution.default
        )

        rotation = (
            module_settings.settings["rotation"]
            if "rotation" in module_settings.settings
            else self.rotation.default
        )

        f.write(
            f"""
services.xserver.displayManager.sddm.enable = true;
services.xserver.displayManager.autoLogin.enable = true;
services.xserver.displayManager.autoLogin.user = "nixos";
services.xserver.windowManager.i3.enable = true;
services.xserver.windowManager.i3.configFile = lib.mkForce (pkgs.writeText "i3-config" ''
# i3 config file (v4)
bar {{
    mode invisible
}}
exec echo 1
# exec "/run/current-system/sw/bin/xrandr --newmode {resolution}_60.00  48.96  1024 1064 1168 1312  600 601 604 622  -HSync +Vsync"
exec echo 2
# exec "/run/current-system/sw/bin/xrandr --addmode HDMI-1 {resolution}_60.00"
exec echo 3
exec "/run/current-system/sw/bin/xrandr --output HDMI-1 --mode {resolution}_60.00"
exec echo 4
exec "/run/current-system/sw/bin/xrandr --output HDMI-1 --rotate {rotation}"
exec "/run/current-system/sw/bin/xset s off"
exec "/run/current-system/sw/bin/xset s off"
exec "/run/current-system/sw/bin/xset -dpms"
exec "${{pkgs.unclutter}}/bin/unclutter"
# exec ${{pkgs.firefox}}/bin/firefox
exec ${{pkgs.firefox}}/bin/firefox --kiosk {kiosk_url}
'');
        """
        )
        f.write(
            f"  systemd.services.display-manager.restartIfChanged = lib.mkForce true;\n"
        )
        f.write(
            f'  systemd.services.display-manager.environment.NONCE = "{kiosk_url}";\n'
        )
