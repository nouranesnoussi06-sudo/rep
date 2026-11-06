let
  rev = "7dcdd87373d72e7a2173e4db02e20d3d7f495cfd";
  sha256 = "09f5ys7xly8gaip09yxpp1xawqm4dlzrjq0ib8x80y9wsdpnp2xl";
in
import (builtins.fetchTarball {
  url = "https://github.com/NixOS/nixpkgs/archive/" + rev + ".tar.gz";
  inherit sha256;
})
