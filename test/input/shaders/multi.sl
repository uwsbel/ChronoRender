surface
multi_one (float Ka = 1;
         float Kd = .5;
         float Ks = .5;
         float roughness = .1;
	 color specularcolor = (1, 0, 0);
     matrix gorb = (1,2,4,5,4,3,2,1);
     )
{
    normal Nf = faceforward (normalize(N),I);
    Oi = Os;
    Ci = Os * ( Cs * (Ka*ambient() + Kd*diffuse(Nf)) +
		specularcolor * Ks*specular(Nf,-normalize(I),roughness));
}

surface
multi_two (float Ka = 1;
         float Kd = .5;
         float Ks = .5;
         float roughness = .1;
	 color specularcolor = (1, 0, 0);
     matrix gorb = (1,2,4,5,4,3,2,1);
     )
{
    normal Nf = faceforward (normalize(N),I);
    Oi = Os;
    Ci = Os * ( Cs * (Ka*ambient() + Kd*diffuse(Nf)) +
		specularcolor * Ks*specular(Nf,-normalize(I),roughness));
}
