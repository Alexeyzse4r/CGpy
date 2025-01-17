

def transforms_3_test():
    from core.transforms.transform import Transform
    from core.vectors import Vec3
    print("=============transforms_3_test=============")
    t = Transform()
    v = Vec3(1, 2, 3)
    t.x = 1.0
    t.y = 4.0
    t.z = 8.0
    t.sx = 2.2
    t.sy = 4.4
    t.sz = 5.5
    t.ax = 15
    t.ay = 30
    t.ay = 60
    print(t)
    v = t.transform_vect(v)
    print(f"v transformed    : {v}")
    v = t.inv_transform_vect(v)
    print(f"v inv transformed: {v}")


def transforms_2_test():
    from core.transforms.transform2 import Transform2
    from core.vectors import Vec2
    print("=============transforms_2_test=============")
    t = Transform2()
    v = Vec2(1, 2)
    t.x = 1.0
    t.y = 4.0
    t.sx = 2.2
    t.sy = 4.4
    t.az = 15
    print(t)
    v = t.transform_vect(v)
    print(f"v transformed    : {v}")
    v = t.inv_transform_vect(v)
    print(f"v inv transformed: {v}")


def surface_test():
    print("=============surface_test=============")
    from core.surface.patch import CubicPatch
    patch = CubicPatch()
    print(patch)
   # print(patch.__mesh)


def bezier_test():
    print("=============bezier_test=============")
    from core.bezier.bezier_curve_3 import BezierCurve3
    from core.vectors import Vec3
    curve = BezierCurve3()
    curve.add_point(Vec3(0, 0, 0), True)
    curve.add_point(Vec3(1, 0, 0), True)
    curve.add_point(Vec3(1, 1, 0), True)
    print(curve)


if __name__ == '__main__':
    transforms_2_test()
    transforms_3_test()
    surface_test()
    bezier_test()

