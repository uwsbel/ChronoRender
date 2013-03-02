surface
plastic (float Ka = 1;
         float Kd = .5;
         float Ks = .5;
         float roughness = .1;
	 color specularcolor = (1, 0, 0);
     )
{
    normal Nf = faceforward (normalize(N),I);
    Oi = Os;
    Ci = Os * ( Cs * (Ka*ambient() + Kd*diffuse(Nf)) +
		specularcolor * Ks*specular(Nf,-normalize(I),roughness));
}

