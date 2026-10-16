
from sqlalchemy import select

from app.db.session import SessionLocal
from app.features.branches.models import Branch


branches = [
    {
        "branch_code": "BR001",
        "name": "Central Branch",
        "address": "Central Street",
    },
    {
        "branch_code": "BR002",
        "name": "North Branch",
        "address": "North Street",
    },
    {
        "branch_code": "BR003",
        "name": "South Branch",
        "address": "South Street",
    },
    {
        "branch_code": "BR004",
        "name": "East Branch",
        "address": "East Street",
    },
    {
        "branch_code": "BR005",
        "name": "West Branch",
        "address": "West Street",
    },
]


def seed_branches():
    db = SessionLocal()

    try:
        for branch_data in branches:
            statement = select(Branch).where(
                Branch.branch_code == branch_data["branch_code"]
            )

            existing_branch = db.scalar(statement)

            if existing_branch is None:
                branch = Branch(**branch_data)
                db.add(branch)
                print(
                    f"Added branch: {branch_data['branch_code']}"
                )
            else:
                print(
                    f"Branch already exists: "
                    f"{branch_data['branch_code']}"
                )

        db.commit()
        print("Branch seeding completed successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_branches()
