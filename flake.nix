{
  description = "AniList readme workflow";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      ...
    }:
    let
      supportedSystems = [
        "aarch64-darwin"
        "x86_64-darwin"
        "x86_64-linux"
      ];
    in
    flake-utils.lib.eachSystem supportedSystems (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            pkgs.python310
            pkgs.python310Packages.pip
            pkgs.git
          ];

          shellHook = ''
            if [ ! -d .venv ]; then
              echo "Creating virtual environment..."
              python -m venv .venv
            fi
            
            source .venv/bin/activate
            
            # Check if requirements.txt has changed
            REQUIREMENTS_HASH=$(sha256sum requirements.txt 2>/dev/null | cut -d' ' -f1 || shasum -a 256 requirements.txt 2>/dev/null | cut -d' ' -f1)
            STORED_HASH=$(cat .venv/.requirements-hash 2>/dev/null || echo "")
            
            if [ ! -f .venv/.requirements-installed ] || [ "$REQUIREMENTS_HASH" != "$STORED_HASH" ]; then
              if [ "$REQUIREMENTS_HASH" != "$STORED_HASH" ] && [ -n "$STORED_HASH" ]; then
                echo "requirements.txt has changed, reinstalling dependencies..."
              else
                echo "Installing dependencies from requirements.txt..."
              fi
              pip install --upgrade pip
              pip install -r requirements.txt
              echo "$REQUIREMENTS_HASH" > .venv/.requirements-hash
              touch .venv/.requirements-installed
            fi
            
            echo "Python: $(python --version)"
            echo "Virtual environment activated"
          '';
        };
      }
    );
}

