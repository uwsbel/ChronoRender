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

surface
occsurf(float samples = 64;
        float maxvariation = 0.02)
{
  //normal Ns = shadingnormal(N);
  normal n = normalize(N);
  normal nf = faceforward(n, I);
  float occ = occlusion(P, nf, samples, 
            "maxvariation", maxvariation,
            "maxdist", 100000);

  Oi = Os;
  Ci = (1 - occ) * Cs * Oi;
}
