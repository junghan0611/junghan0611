{
  description = "Public AX evidence dossier — one Org SSOT to web, PDF, and Markdown";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { nixpkgs, ... }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" ];
      forAll = nixpkgs.lib.genAttrs systems;
    in {
      devShells = forAll (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          tex = pkgs.texlive.combine {
            inherit (pkgs.texlive)
              scheme-medium
              collection-latexextra
              latexmk
              acmart
              newtx
              libertine
              xetexko
              kotex-utf;
          };

          # Noto Sans CJK ships one variable-weight TTC per script set, and xetexko cannot
          # index into it — XeLaTeX stops at `Invalid TTC index number`. Pretendard installs
          # static OTFs, one face per file, which is what resolution by family name needs.
          fonts = [ pkgs.pretendard pkgs.d2coding ];

          # The shell must not inherit the host's font cache. A PDF whose Hangul resolves
          # only on a machine that happens to have the family installed is not reproducible,
          # and the failure is silent — XeTeX substitutes and the page still renders. Pinning
          # FONTCONFIG_FILE to the closure makes the font set part of the build inputs.
          fontsConf = pkgs.makeFontsConf { fontDirectories = fonts; };
        in {
          default = pkgs.mkShell {
            packages = [
              pkgs.emacs
              pkgs.pandoc
              pkgs.gnumake
              pkgs.poppler-utils
              pkgs.fontconfig
              tex
            ] ++ fonts;

            FONTCONFIG_FILE = fontsConf;
          };
        });
    };
}
