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
envlight(
    float samples = 64, maxvariation = 0.02;
    string envmap = "";
    float maxdist = 1;
    float coneangle = 0.785;
    color filter = color(1);
    output float __nonspecular = 1;)
{
  normal Ns = shadingnormal(N);

  illuminate (Ps + Ns) {
      color irrad = 0;
      float occ = occlusion(Ps, Ns, samples, 
              "maxvariation", maxvariation,
              "maxdist", maxdist,
              "coneangle", coneangle
              "environmentmap", envmap,
              "environmentcolor", irrad
              ); 
      Cl = filter * irrad;
  }
}
