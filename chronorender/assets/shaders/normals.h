/* $Id: //depot/main/rmanprod/rman/shaders/shadingnormal.sl#0 $  (Pixar - RenderMan Division)  $Date: 2002/10/29 $ */
/*
** Copyright (c) 2002-2012 PIXAR.  All rights reserved.  This program or
** documentation contains proprietary confidential information and trade
** secrets of PIXAR.  Reverse engineering of object code is prohibited.
** Use of copyright notice is precautionary and does not imply
** publication.
**
**                      RESTRICTED RIGHTS NOTICE
**
** Use, duplication, or disclosure by the Government is subject to the
** following restrictions:  For civilian agencies, subparagraphs (a) through
** (d) of the Commercial Computer Software--Restricted Rights clause at
** 52.227-19 of the FAR; and, for units of the Department of Defense, DoD
** Supplement to the FAR, clause 52.227-7013 (c)(1)(ii), Rights in
** Technical Data and Computer Software.
**
** Pixar
** 1200 Park Avenue
** Emeryville, CA 94608
*/

/*
 * Compute normalized shading normal with appropriate orientation.
 * We ensure that the normal faces forward if Sides is 2 or if the 
 * shader evaluation is caused by a ray hit.
 *
 * So we only adhere to the object's surface orientation if Sides is 1
 * and we're on a REYES micropolygon grid.  Why, you may ask, would a
 * point be shaded if it is facing away and Sides is 1?  Isn't that
 * exactly what Sides 1 should disallow?  The reason is that points
 * on grids that have both forward and backward facing points do get
 * shaded even if Sides is 1.  It's only if the entire micropolygon
 * grid is facing away that it doesn't get shaded.
 *
 * Why do we want to adhere to the surface orientation if Sides is 1?
 * Why not just always flip the normal forward with the faceforward()
 * call?  The reason is that this would mean that some points on some
 * REYES micropolygon grids would have unintended normals.  If we 
 * shade a point with the shading result for the wrong side of the
 * surface, the color can be wrong, giving artifacts along silhouette
 * edges where the color is interpolated between shading points that
 * face forward and shading points that face backward.  Also, in some 
 * cases, the shading computation on the "wrong" side might be much
 * more expensive than on the "right" side.
 */
normal
shadingnormal(normal N)
{
    normal Ns = N;
    uniform float sides = 2;
    uniform float raydepth;
    attribute("Sides", sides);
    rayinfo("depth", raydepth);
    if (sides == 2 || raydepth > 0)
	Ns = faceforward(Ns, I, Ns);
    return normalize(Ns);
}
