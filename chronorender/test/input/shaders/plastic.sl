surface
plastic (float Ka = 1;
         float Kd = .5;
         float Ks = .5;
         float roughness = .1;
	 color specularcolor = (1, 0, 0);
     matrix blarg = (1,2,4,5,4,3,2,1);
     )
{
    normal Nf = faceforward (normalize(N),I);
    Oi = Os;
    Ci = Os * ( Cs * (Ka*ambient() + Kd*diffuse(Nf)) +
		specularcolor * Ks*specular(Nf,-normalize(I),roughness));
}

