normal

shadingnormal(normal N)

{

    extern vector I;

    normal Ns = normalize(N);

    uniform float sides = 2;

    uniform float raydepth;

    attribute("Sides", sides);

    rayinfo("depth", raydepth);

    if (sides == 2 || raydepth > 0)

  Ns = faceforward(Ns, I, Ns);

    return Ns;

}
light
indirectlight(
  float samples = 64, maxvariation = 0.02;
  string envmap = "";
  color filter = color(1);
  output float __nonspecular = 1;)
{
  normal Ns = shadingnormal(N);

  /* Compute indirect diffuse illumination */
  illuminate (Ps + Ns) {  /* force execution independent of light location */
    Cl = filter * indirectdiffuse(Ps, Ns, samples, "maxvariation", maxvariation,
                                  "environmentmap", envmap);
  }
}
