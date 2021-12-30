from dataclasses import dataclass
import requests


@dataclass
class Client:
    url: str
    headers: dict

    def run_query(self, query: str, variables: dict, extract=False):
        request = requests.post(
            self.url,
            headers=self.headers,
            json={"query": query, "variables": variables},
        )
        assert request.ok, f"Failed with code {request.status_code}"
        return request.json()

    def post_time_in(self, id, clock_in):  # Inserts clocked in time to db
        time_in = self.fetch_time_in(id)
        formatted_time = time_in['data']['dawn_by_pk']['clock_in']
        # if (formatted_time != clock_in):
        #     print("Yo the time is equal")
        #     self.run_query(
        #         """
        #     mutation ($id: Int!, $clock_in: time!) {
        #         update_dawn(where: {id: {_lte: $id}}, _set: { clock_in: $clock_in }) {
        #             affected_rows
        #             returning {
        #                 id
        #                 clock_in
        #             }
        #         }
        #     }
        #     """
        #     )
        # else:
        self.run_query(
            """
        mutation ($id: Int!, $clock_in: time!) {
            insert_dawn_one(objects: {id: $id, clock_in: $clock_in}) {
                affected_rows
                returning {
                    id
                    clock_in
                }
            }
        }
        """,
            {'id': id, 'clock_in': clock_in}
        )

    def fetch_all_entries(self):
        self.run_query(
            """
                query fetch_clock_in {
                        dawn {
                            clock_in
                            id
                        }
                }
            """
        )

    def fetch_by_id_from_dawn(self, id):
        return self.run_query(
            """ 
            query fetch_by_id($id: Int!) {
                dawn_by_pk(id: $id) {
                    clock_in
                }
            }
            """,
            {'id': id}
        )

    def fetch_by_id_from_dusk(self, id):
        return self.run_query(
            """
            query fetch_by_id($id: Int!) {
                dusk_by_pk(id: $id) {
                    clock_in
                }
            }
            """,
            {'id': id}
        )
