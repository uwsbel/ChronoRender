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
occlusionlight2(
    float samples = 64, maxvariation = 0.05;
    color filter = color(1);
    output float __nonspecular = 1;)
{
  normal Ns = shadingnormal(N);

  illuminate (Ps + Ns) {
    float occ = occlusion(Ps, Ns, samples, "maxvariation", 0.0); 
    Cl = filter * (1 - occ);
  }
}
