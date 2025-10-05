from ppl import Variable, Constraint, Constraint_System, C_Polyhedron


def main():
    # Define variables (order: x, y, u, v)
    x = Variable(0)
    y = Variable(1)
    u = Variable(2)
    v = Variable(3)

    # Build the constraint system Ax >= b for polyhedron P
    cs = Constraint_System()

    # Constraints:
    cs.insert(x >= 0)
    cs.insert(x <= 1)
    cs.insert(y >= 0)
    cs.insert(y <= 1)
    cs.insert(u >= 0)
    cs.insert(v >= 0)
    cs.insert(u - v <= 0)
    cs.insert(x + y <= 2)

    # Construct polyhedron
    P = C_Polyhedron(cs)

    # Get extreme points and extreme rays
    gen = P.generators()

    extreme_points = [g for g in gen if g.is_point()]
    extreme_rays   = [g for g in gen if g.is_ray()]

    print("Extreme points:")
    for p in extreme_points:
        print(p)

    print("\nExtreme rays:")
    for r in extreme_rays:
        print(r)

    # Get minimal (facet-defining) constraints
    facets = P.minimized_constraints()

    print("\nFacet-defining inequalities:")
    for f in facets:
        print(f)


if __name__ == "__main__":
    main()