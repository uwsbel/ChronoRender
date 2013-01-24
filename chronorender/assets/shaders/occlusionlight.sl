normal
shadingnormal(normal N)
{
    normal Ns = normalize(N);
    uniform float sides = 2;
    uniform float raydepth;
    attribute("Sides", sides);
    rayinfor("depth", raydepth);
    if (sides == 2 || raydepth > 0)
        Ns = faceforward(Ns, I, Ns);
    return Ns;
}

light
occlusionlight(float samples = 64; 
               float maxvariation = 0.02;
               color filter = color(1);
               output float __nonspecular = 1;
               )
{
    normal Ns = shadingnormal(N);
    illuminate (Ps + Ns) {
        float occ = occlusion(Ps, Ns, samples, "maxvariation", maxvariation);
        Cl = filter * (1-occ);
    }
}
