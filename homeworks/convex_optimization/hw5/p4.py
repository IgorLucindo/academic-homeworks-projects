import numpy as np
from mosek.fusion import Model, Domain, Expr, Matrix, ObjectiveSense


def solve_stochastic_program():
    n = 10
    h = 10.0
    p = 11.0
    dvals = np.arange(10, 16)          # {10, 11, 12, 13, 14, 15}
    D = len(dvals)
    prob = 1.0 / D                     # uniform on the 6 values

    with Model("SP_newsvendor") as M:
        # Decision variables
        x  = M.variable("x", 1, Domain.greaterThan(0.0))   # scalar x >= 0 (1-dim)
        u  = M.variable("u", D, Domain.greaterThan(0.0))   # u_d >= 0
        v  = M.variable("v", D, Domain.greaterThan(0.0))   # v_d >= 0

        # Column of demands
        dcol = Matrix.dense(dvals.reshape(-1, 1))

        # Broadcast x to length-D vector: x_rep[i] = x for all i
        ones = Matrix.dense(np.ones((D, 1)))
        x_rep = Expr.mul(ones, x)      # (D x 1) * (1) -> (D)

        # u_d >= x - d  <=> x_rep - dcol - u <= 0
        M.constraint(
            "u_ge_x_minus_d",
            Expr.sub(Expr.sub(x_rep, dcol), u),
            Domain.lessThan(0.0)
        )

        # v_d >= d - x  <=> dcol - x_rep - v <= 0
        M.constraint(
            "v_ge_d_minus_x",
            Expr.sub(Expr.sub(dcol, x_rep), v),
            Domain.lessThan(0.0)
        )

        # Expected cost per item: (1/6) sum_d (h u_d + p v_d)
        cost_per_item = Expr.mul(prob,
                                 Expr.add(Expr.mul(h, Expr.sum(u)),
                                          Expr.mul(p, Expr.sum(v))))

        # Total cost for n items
        total_cost = Expr.mul(n, cost_per_item)

        M.objective("obj", ObjectiveSense.Minimize, total_cost)
        M.solve()

        x_opt   = x.level()[0]
        obj_opt = M.primalObjValue()

        return x_opt, obj_opt
    

def solve_dro_moment():
    n = 10
    h = 10.0
    p = 11.0
    dvals = np.arange(10, 16)      # {10,...,15}
    D = len(dvals)

    # Moments of discrete uniform {10,...,15}
    mu = np.mean(dvals)
    var = np.var(dvals, ddof=0)    # population variance
    sigma = np.sqrt(var)

    lam1 = 2.0
    lam2 = 2.0

    with Model("DRO_newsvendor") as M:
        # Decision variables
        x     = M.variable("x", 1, Domain.greaterThan(0.0))
        alpha = M.variable("alpha", 1, Domain.unbounded())
        q     = M.variable("q", 1, Domain.unbounded())
        qabs  = M.variable("qabs", 1, Domain.greaterThan(0.0))
        Q     = M.variable("Q", 1, Domain.greaterThan(0.0))

        # u_d, v_d to represent (x-d)_+ and (d-x)_+
        u = M.variable("u", D, Domain.greaterThan(0.0))
        v = M.variable("v", D, Domain.greaterThan(0.0))

        dcol = Matrix.dense(dvals.reshape(-1, 1))
        ones = Matrix.dense(np.ones((D, 1)))
        x_rep = Expr.mul(ones, x)

        # u_d >= x - d  <=> x_rep - dcol - u <= 0
        M.constraint(
            "u_ge_x_minus_d",
            Expr.sub(Expr.sub(x_rep, dcol), u),
            Domain.lessThan(0.0)
        )

        # v_d >= d - x  <=> dcol - x_rep - v <= 0
        M.constraint(
            "v_ge_d_minus_x",
            Expr.sub(Expr.sub(dcol, x_rep), v),
            Domain.lessThan(0.0)
        )

        # qabs >= |q|
        # qabs >= q  => q - qabs <= 0
        M.constraint(
            "qabs_ge_q",
            Expr.sub(q, qabs),
            Domain.lessThan(0.0)
        )
        # qabs >= -q => -q - qabs <= 0
        M.constraint(
            "qabs_ge_minusq",
            Expr.add(Expr.neg(q), Expr.neg(qabs)),
            Domain.lessThan(0.0)
        )

        # Dual constraints, one per scenario d
        for i, d in enumerate(dvals):
            # RHS: h*u_i + p*v_i
            rhs = Expr.add(Expr.mul(h, u.index(i)),
                           Expr.mul(p, v.index(i)))

            # LHS: alpha - (d/sigma)*q + (d - mu)^2 * Q
            lhs = Expr.sub(alpha, Expr.mul(d / sigma, q))
            lhs = Expr.add(lhs, Expr.mul((d - mu) ** 2, Q))

            # lhs >= rhs  <=> rhs - lhs <= 0
            M.constraint(
                f"dual_ineq_{d}",
                Expr.sub(rhs, lhs),
                Domain.lessThan(0.0)
            )

        # Per-item objective from dual
        per_item_obj = Expr.add(
            alpha,
            Expr.add(
                Expr.mul(-mu / sigma, q),
                Expr.add(
                    Expr.mul(np.sqrt(lam1), qabs),
                    Expr.mul(lam2 * var, Q)
                )
            )
        )

        total_obj = Expr.mul(n, per_item_obj)

        M.objective("obj", ObjectiveSense.Minimize, total_obj)
        M.solve()

        x_opt   = x.level()[0]
        obj_opt = M.primalObjValue()

        return x_opt, obj_opt
    

def main():
    x_sp,  obj_sp  = solve_stochastic_program()
    x_dro, obj_dro = solve_dro_moment()

    print("\nComparison:")
    print(f"  SP  : x* = {x_sp:.4f},  total cost = {obj_sp:.4f}")
    print(f"  DRO : x* = {x_dro:.4f}, total cost = {obj_dro:.4f}")


if __name__ == "__main__":
    main()