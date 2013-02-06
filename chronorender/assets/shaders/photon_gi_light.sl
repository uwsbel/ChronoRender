normal shadingnormal(normal N) {
  normal Ns = N;
  uniform float raydepth;
  uniform float sides;
  attribute("Sides", sides);
  rayinfo("depth", raydepth);
  if (sides == 2 || raydepth > 0)
    Ns = faceforward(Ns, I, Ns);
  return normalize(Ns);
}

light
photon_gi_light(
    float samples = 64, maxvariation = 0.02;
    color filter = color(1);
    output float __nonspecular = 1;)
{
  normal Ns = shadingnormal(N);

  illuminate (Ps + Ns) {
      color radio = 0;
      texture3d(causticmap, Ps, Ns, "_radiosity", radio);
      Cl = radio;
  }
}
