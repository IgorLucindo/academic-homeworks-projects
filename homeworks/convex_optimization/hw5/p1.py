import numpy as np
from mosek.fusion import Model, Domain, Expr, Matrix, ObjectiveSense, SolutionStatus, ProblemStatus

# ------------------------------------------------
# Problem/data setup
# ------------------------------------------------
np.random.seed(0)

d = 50        # number of data points
p = 3         # dimension of x
R = 1.0       # radius parameter for C = { (x,t) : ||x||_2 <= t }, here t = R (fixed)

# Random features
X = np.random.randn(d, p)

# Ground-truth linear separator (just to generate labels)
w_true = np.random.randn(p)
b_true = 0.5

# Labels in {-1, +1}
margins = X @ w_true + b_true
y = np.sign(margins)
y[y == 0] = 1.0
y = y.astype(float)

# Constant matrices for MOSEK
Xmat  = Matrix.dense(X)                  # (d, p)
y_mat = Matrix.dense(y.reshape(d, 1))    # (d, 1)
ones  = Matrix.dense(np.ones((d, 1)))    # (d, 1), used to broadcast b


def solve_primal_and_dual():
    """
    Build the primal problem, let MOSEK solve it,
    and read both the primal and dual objective values
    from the same model.
    """
    with Model("primal") as M:
        w  = M.variable("w",  p, Domain.unbounded())
        b  = M.variable("b",  1, Domain.unbounded())
        u  = M.variable("u",  d, Domain.unbounded())
        r1 = M.variable("r1", d, Domain.unbounded())
        r2 = M.variable("r2", d, Domain.unbounded())

        M.objective("obj", ObjectiveSense.Minimize, Expr.sum(u))

        M.constraint("r_sum", Expr.add(r1, r2), Domain.lessThan(1.0))
        xw = Expr.mul(Xmat, w)                      # (d,1) = X w
        xw = Expr.add(xw, Expr.mul(ones, b))        # + b

        M.constraint("exp1", Expr.hstack(r1, Expr.constTerm(d, 1.0), Expr.neg(u)), Domain.inPExpCone())

        y_xw  = Expr.mulElm(y_mat, xw)         # (d,1) = y_i(<x_i,w>+b)
        inner = Expr.sub(Expr.neg(u), y_xw)    # (-u_i - y_i(<x_i,w>+b))

        M.constraint("exp2", Expr.hstack(r2, Expr.constTerm(d, 1.0), inner), Domain.inPExpCone())
        M.constraint("C", Expr.vstack(Expr.constTerm(1, R), w), Domain.inQCone())

        M.solve()

        # Only access objective values if both primal and dual are feasible/optimal
        if (M.getProblemStatus() == ProblemStatus.PrimalAndDualFeasible and
            M.getPrimalSolutionStatus() == SolutionStatus.Optimal and
            M.getDualSolutionStatus()   == SolutionStatus.Optimal):

            primal_obj = M.primalObjValue()
            dual_obj   = M.dualObjValue()

            print("Primal optimal value:", primal_obj)
            print("Dual   optimal value:", dual_obj)
            print("Duality gap (P - D):", primal_obj - dual_obj)

            # Optional: return everything
            return {
                "w":         w.level(),
                "b":         b.level()[0],
                "u":         u.level(),
                "r1":        r1.level(),
                "r2":        r2.level(),
                "primal_obj": primal_obj,
                "dual_obj":   dual_obj
            }
        else:
            print("\nModel did not return primal+dual optimal solutions.")
            return None


def main():
    solve_primal_and_dual()


if __name__ == "__main__":
    main()