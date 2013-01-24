surface
occlusionsurf(float samples = 64; 
               float maxvariation = 0.02)
{
    normal Ns = N;
    float occ = occlusion(Ps, Ns, samples, "maxvariation", maxvariation);

    Ci = (1-occ) * Cs * Os;
    Oi = Os;
}
