def test_unicode(testdir):
    # Unicode identifyers are in fact legal Python code
    string = """
    ```python
    # Α α, Β β, Γ γ, Δ δ, Ε ε, Ζ ζ, Η η, Θ θ, Ι ι, Κ κ, Λ λ, Μ μ, Ν ν, Ξ ξ, Ο ο, Π π,
    # Ρ ρ, Σ σ/ς, Τ τ, Υ υ, Φ φ, Χ χ, Ψ ψ, Ω ω
    α = 1
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)
